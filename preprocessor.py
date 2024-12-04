import datetime
import re
import pandas as pd


def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{1,2},\s\d{1,2}:\d{1,2}\s?(?:am|pm)\s-\s'

    # Extract messages and dates
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # Convert date strings to 24-hour format
    dates = [
        datetime.datetime.strptime(date.rstrip()[:-2].replace('\u202f', ' '), "%d/%m/%y, %I:%M %p").strftime(
            "%d/%m/%y %H:%M")
        for date in dates
    ]

    # Create DataFrame using converted dates
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Convert 'message_date' column to datetime format
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y %H:%M')
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Separate users and messages
    users = []
    msgs = []
    for message in df['user_message']:
        entry = re.split(r'([\w\w]+?):\s', message)
        if len(entry) > 2:  # If user and message are present
            users.append(entry[1])
            msgs.append(entry[2])
        else:
            users.append('group_notification')
            msgs.append(entry[0])

    df['user'] = users
    df['message'] = msgs

    # Drop the original 'user_message' column
    df.drop(columns=['user_message'], inplace=True)

    # Add additional time-related columns
    df['year'] = df['date'].dt.year
    df['only_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))
    df['period'] = period
    return df
