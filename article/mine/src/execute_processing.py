from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.metrics.pairwise import cosine_similarity

import pandas as pd

from sqlite_utils import get_news, get_reddit_posts, get_tweets
from utils import get_summary, get_tweet_creation_date, project


news_list = get_news()
news_list = list(map(lambda x : {**x, 'summary': get_summary(x['content']), }, news_list))

example_news = news_list[0]

tweet_list = get_tweets()
tweet_list = list(map(lambda x : {**x, 'created_date_time': get_tweet_creation_date(int(x['id'])), 'id' : 't-'+ x['id'], 'relevance': 1 if int(x['ranking']) > 0 else 0}, tweet_list))

reddit_posts_list = get_reddit_posts()
reddit_posts_list = list(map(lambda x : {**x, 'summary': get_summary(x['body']), }, reddit_posts_list))
reddit_posts_list = list(map(lambda x : {**x, 'all_infos': ' '.join([x['subreddit'], x['author'], x['body']]), 'relevance': 0 }, reddit_posts_list))

def get_relevance(data_src, data_id, news_id):
    if(data_src == 'tweets'):
        filtered = list(filter(lambda x: x['id'] == data_id and x['related_news_id'] == news_id, tweet_list))

        if(len(filtered)>0):
            return filtered[0]['relevance']

    return 0

def get_similarities(data_src, data_prop, news_prop):
    vectorizer = Pipeline([('count', CountVectorizer()),
                      ('tfid', TfidfTransformer())])

    data = tweet_list if data_src == 'tweets' else reddit_posts_list

    news_len = len(news_list)
    data_len = len(data)
    
    merged_corpus = list(project(news_list, news_prop))
    merged_corpus.extend(project(data, data_prop))

    vetores = vectorizer.fit_transform(merged_corpus)
    tfidf_matrix = vetores.toarray()

    similarities = []

    news_we = tfidf_matrix[0: news_len, :]

    data_we = tfidf_matrix[news_len: len(tfidf_matrix), :]

    sim = cosine_similarity(news_we, data_we)

    for ni in range(0, news_len):
        news_id = news_list[ni]['id']
        
        for di in range(0, data_len):
            data_id = data[di]['id']

            relevance = get_relevance(data_src, data_id, news_id)

            obj = {
                'news_id': news_id,
                'news_prop': news_prop,
                'data_id': data_id,
                'data_src': data_src,
                'data_prop': data_prop,
                'sim':  sim[ni][di],
                'relevance': relevance
            }

            similarities.append(obj)
    
    return similarities

scores = []

news_props = ['content', 'title', 'summary']
data_srcs = [('tweets', 'content'), ('reddit', 'body')]

for news_prop in news_props:
    print("news_prop", news_prop)
    for src in data_srcs:
        scores.extend(get_similarities(src[0], src[1], news_prop))

scores_df = pd.DataFrame(scores)

annotated_news_ids = map(lambda x: x['related_news_id'], filter(lambda x: x['relevance'] > 0, tweet_list))

metrics = []

for n in annotated_news_ids:
    for src in data_srcs:
        if src[0] == 'tweets':
            relevant_documents = list(filter(lambda x: x['related_news_id'] == n and x['relevance'] > 0, tweet_list))
        else:
            relevant_documents = []

        for p in news_props:
            r = {
                'news_id': n,
                'data_src': src[0],
                'news_prop': p
            }
            
            ranked_documents = scores_df[(scores_df['news_id'] == n) & (scores_df['data_src'] == src[0]) & (scores_df['news_prop'] == p)]
            
            ranked_documents.sort_values('sim', ascending=False, inplace=True)

            #considerando os 10 primeiros documentos como a resposta da RI
            first_10 = ranked_documents[0:10]

            ids = list(first_10['news_id'].unique())
            
            relevant_retrieved = list(filter(lambda id: len(list(filter(lambda rd: rd['related_news_id']==id, relevant_documents))) > 0, ids))

            r['precision'] = len(relevant_retrieved)/len(first_10)

            r['recall'] = 0 if len(relevant_documents) == 0 else len(relevant_retrieved)/len(relevant_documents)

            p_10 = len(first_10[first_10['relevance'] > 0]) / len(first_10)

            r['p_10'] = p_10

            first_5 = first_10[0:5]

            p_5 = len(first_5[first_5['relevance'] > 0]) / len(first_5)

            r['p_5'] = p_5

            metrics.append(r)

metrics_df = pd.DataFrame(metrics)

average_metrics = []

metric_values = ['precision', 'p_5', 'p_10']

for src in data_srcs:
    for p in news_props:
        am = {
            'data_src': src[0],
            'news_prop': p
        }

        filtered_metrics = metrics_df[(metrics_df['data_src'] == src[0]) & (metrics_df['news_prop'] == p)]

        for mv in metric_values:
            am[mv] = filtered_metrics[mv].mean()
        
        average_metrics.append(am)

average_metrics_df = pd.DataFrame(average_metrics)

average_metrics_df.to_csv('average_metrics.csv')

metrics_df.to_csv('metrics.csv',)

scores_df.to_csv('scores.csv',)