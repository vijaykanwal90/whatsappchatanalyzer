
import matplotlib.pyplot as plt
import streamlit as st
import preprocessor  # Assuming preprocessor is a module containing your preprocess function
import helper
from wordcloud import WordCloud
import seaborn as sns
st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:

    # Read file and decode
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

    # Debug: Show the first 500 characters
    # st.text(data[:500])

    # Preprocess data
    df = preprocessor.preprocess(data)

    # Display the dataframe
    # st.dataframe(df)
    #   fetch unique user
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user =  st.sidebar.selectbox("Show analysis wrt",user_list)
    if st.sidebar.button("Show Analysis"):
        # Stats Area
        num_messages, words, num_media_messages, links = helper.fetch_stats(selected_user,df)
        st.title("Top statistics")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total message")
            st.title(num_messages)
        with col2:
            st.header("Total words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Link Shared")
            st.title(links)

        # monthly timeline
        st.title("Monthly timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Daily Timeline
        st.title("Daily timeline")
        daily = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily['only_date'], daily['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map
        st.title("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig, ax = plt.subplots( )
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user,df)
            fig, ax = plt.subplots( )
            ax.bar(busy_month.index, busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        # activity heatmap
        st.title("Weekly Activity")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap,linewidth=.5)
        st.pyplot(fig)
        # finding the busiest users in the group( group level)
        if selected_user =='Overall':
            st.title("Most Busy Users")
            x,new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)
            with col1:
                ax.bar(x.index, x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # wordcloud
        st.title("Word Cloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig,ax  = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
    # most common words
        most_common_df = helper.most_common_words(selected_user,df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title('Most common words')
        st.pyplot(fig)
        # st.dataframe(most_common_df)

        st.title("Sentiment Analysis")
        df_sentiment,compound_stmt = helper.analyze(df)
        sentiment_percentage = df_sentiment * 100

        # Format the sentiment percentage to 2 decimal places
        sentiment_percentage_str = f"{sentiment_percentage:.2f}%"
        col1, col2 = st.columns(2)
        with col1:
            st.header("Sentiment Score")
            st.title(sentiment_percentage_str)
        with col2:
            st.header("Positivity Score")
            st.title(compound_stmt)





