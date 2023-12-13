import sqlite3

SQLITE_FILE = 'C:\\Users\\guiav\\Source_Code\\repos\\rec-info-20232\\article\\data\\data-sqlite'

sqliteConnection = sqlite3.connect(SQLITE_FILE)

def get_tweets():
    cursor = sqliteConnection.cursor()

    query = 'select t.content, t.id, t.related_news_id, t.ranking from tweets t order by t.id asc'

    cursor = sqliteConnection.execute(query)

    tweets = cursor.fetchall()

    return list(map(lambda t: {'content': t[0], 'id': t[1], 'related_news_id': t[2], 'ranking': t[3]}, tweets))


def get_news():
    cursor = sqliteConnection.cursor()

    query = 'select n.title, n.content, n.title, n.source, n.published, n.id from news_samples n'

    cursor = sqliteConnection.execute(query)

    news = cursor.fetchall()

    return list(map(lambda t: {'title': t[0], 'content': t[1], 'title': t[2], 'source': t[3], 'published': t[4], 'id': t[5]}, news))

def get_reddit_posts():
    cursor = sqliteConnection.cursor()

    query = """SELECT
                subreddit,
                author,
                body,
                created_utc,
                author_flair_text,
                id
            FROM
                reddit_samples"""

    cursor = sqliteConnection.execute(query)

    posts = cursor.fetchall()

    return list(map(lambda t: {'subreddit': t[0], 'author': t[1], 'body': t[2], 'created_utc': t[3], 'author_flair_text': t[4], 'id': t[5]}, posts))

def get_news_cursor() -> sqlite3.Cursor:
    cursor = sqliteConnection.cursor()

    query = 'select n.title, n.content, n.title, n.source, n.published, n.id from news_samples n'

    cursor = sqliteConnection.execute(query)

    return cursor

def map_news_cursor_to_object(news):
    return list(map(lambda t: {'title': t[0], 'content': t[1], 'title': t[2], 'source': t[3], 'published': t[4], 'id': t[5]}, news))

def get_cursor():
    return sqliteConnection.cursor()

def commit():
    sqliteConnection.commit()

def upsert_cosine_sim_news_content(tweet_id, news_id, sim, cursor = None):
    if(cursor == None):
        cursor = sqliteConnection.cursor()

    result = cursor.execute('select exists (select * from tweet_news where tweet_id = ? and news_id = ?)', (tweet_id, news_id)).fetchone()

    if(result[0] == False):
        cursor.execute('insert into tweet_news(tweet_id, news_id) values (?, ?)', (tweet_id, news_id))

    cursor.execute('update tweet_news set cosine_sim_news_content = ? where tweet_id = ? and news_id = ?', (sim, tweet_id, news_id))