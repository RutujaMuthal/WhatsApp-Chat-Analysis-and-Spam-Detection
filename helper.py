from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
extract = URLExtract()
def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    num_messages = df.shape[0]
    # fetch the total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # fetch number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    # fetch number of links shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)


def shared_links_df_simple(df):
    links_list = []

    for message in df['message']:
        links = extract.find_urls(message)
        links_list.extend(links)

    links_df = pd.DataFrame(links_list,columns=['links'])
    new_user = df[['user']]

    links_df['key']= 1
    new_user['key'] = 1

    result_df=pd.merge(new_user,links_df,on='key').drop('key',axis=1)
    result_df1 = result_df.loc[result_df['user'] != 'group_notification']
    df_unique = result_df1.drop_duplicates()
    return df_unique
def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x, df
def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    wc = WordCloud(width = 500, height = 500, min_font_size = 10, background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc
def most_common_words(selected_user, df):
    
    with open('stop_hinglish.txt', 'r', encoding='utf-8') as f:
        stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

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
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline
def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_time').count()['message'].reset_index()

    return daily_timeline
def load_file_to_list(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = [line.strip() for line in file.readlines()]
    return lines

# Example usage
file_path = 'spam_keyword.txt'
spam_keyword = load_file_to_list(file_path)
print(spam_keyword)

def classify_message(message):

        message_lower = str(message).lower()
        if not any(keyword in message_lower for keyword in spam_keyword):
            return 'ham'
        else:
            return 'spam'
        df['classification'] = df['message'].apply(classify_message)
        return df
