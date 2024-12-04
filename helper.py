# from pygments.styles.dracula import background
from wordcloud import WordCloud
from urlextract import URLExtract
import pandas as pd
from collections import Counter
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer
def fetch_stats(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    # fetch the number of messages
    num_messages = df.shape[0]
    # fetch the number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # fetch the number of media
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]
    links = []
    extractor = URLExtract()
    for message in df['message']:
        urls = extractor.find_urls(message)
        links.extend(urls)
    # link_shared = df[df['message']] == ''].shape[0]
    return num_messages, len(words), num_media_messages, len(links)

def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round(df['user'].value_counts()/df.shape[0] * 100,2).reset_index().rename(columns={'user':'name'})

    return x,df

def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    wc = WordCloud(width=500,height=500, min_font_size=10,background_color='white')
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user, df):
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()
    if selected_user != 'Overall':
       df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    print(temp)

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    df['month_num'] = df['date'].dt.month
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily = df.groupby('only_date').count()['message'].reset_index()
    return daily

def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return user_heatmap

def analyze(df):
    sia = SentimentIntensityAnalyzer()
    df['sentiment_scores'] = df['message'].apply(lambda message: sia.polarity_scores(message))


    # Extract the 'compound' score into a separate column
    df['compound'] = df['sentiment_scores'].apply(lambda score: score['compound'])

    # Calculate the overall sentiment (average of the 'compound' score)
    overall_sentiment = df['compound'].mean()

    # Display the DataFrame with sentiment scores

    # Display the overall sentiment (compound score)
    print(f"\nOverall Sentiment (Compound Score): {overall_sentiment}")
    compound_stmt="Positive"
    # Interpretation of the overall sentiment
    if overall_sentiment >= 0.05:
        # print("Overall sentiment is Positive")
        compound_stmt="Positive"
    elif overall_sentiment <= -0.05:
        compound_stmt="Negative"

        # print("Overall sentiment is Negative")
    else:
        # print("Overall sentiment is Neutral")
        compound_stmt="Neutral"


    return overall_sentiment, compound_stmt