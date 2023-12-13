from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from utils import  get_summary, get_token_count, project, get_distinct_token_count

import pandas as pd

from tokenizers import Tokeniser
from sqlite_utils import get_news, get_reddit_posts, get_tweets

tokeniser = Tokeniser()

news_list = get_news()
news_list = list(map(lambda x : {**x, 'summary': get_summary(x['content']), }, news_list))
news_content_list = project(news_list, 'content')

total_news_content_tokens = sum(map(lambda x : get_token_count(x), news_content_list))

print('Total news tokens(content): ' + str(total_news_content_tokens))
print('Average news tokens(content): ' + str(total_news_content_tokens/len(news_content_list)))
print('Distinct news tokens(content): ' + str(get_distinct_token_count(news_content_list)))
print()

news_title_list = project(news_list, 'title')

total_news_title_tokens = sum(map(lambda x : get_token_count(x), news_title_list))

print('Total news tokens(title): ' + str(total_news_title_tokens))
print('Average news tokens(title): ' + str(total_news_title_tokens/len(news_title_list)))
print('Distinct news tokens(title): ' + str(get_distinct_token_count(news_title_list)))
print()

news_summary_list = project(news_list, 'summary')

total_news_summary_tokens = sum(map(lambda x : get_token_count(x), news_summary_list))

print('Total news tokens(summary): ' + str(total_news_summary_tokens))
print('Average news tokens(summary): ' + str(total_news_summary_tokens/len(news_summary_list)))
print('Distinct news tokens(summary): ' + str(get_distinct_token_count(news_summary_list)))
print()

tweet_list = get_tweets()

total_tweet_tokens = sum(map(lambda x : get_token_count(x), project(tweet_list, 'content')))

print('Total tweet tokens(content): ' + str(total_tweet_tokens))
print('Average tweet tokens(content): ' + str(total_tweet_tokens/len(tweet_list)))
print('Distinct tweet tokens(content): ' + str(get_distinct_token_count(project(tweet_list, 'content'))))
print()

reddit_posts_list = get_reddit_posts()

total_reddit_tokens = sum(map(lambda x : get_token_count(x), project(reddit_posts_list, 'body')))

print('Total reddit comments tokens(body): ' + str(total_reddit_tokens))
print('Average reddit comments tokens(body): ' + str(total_reddit_tokens/len(reddit_posts_list)))
print('Distinct reddit comments tokens(body): ' + str(get_distinct_token_count(project(reddit_posts_list, 'body'))))
print()

# reddit_posts_list = get_reddit_posts()
