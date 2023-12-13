import json
import sqlite3
import random

file_path = 'C:\\Users\\guiav\\Source_Code\\repos\\rec-info-20232\\article\\data\\reddit\\RC_2015-08\\RC_2015-08'

sqliteConnection = sqlite3.connect('C:\\Users\\guiav\\Source_Code\\repos\\rec-info-20232\\article\\data\\data-sqlite')
cursor = sqliteConnection.cursor()
print("Successfully Connected to SQLite")

c = 0

tq = 58075327

dq = 5000

with open(file_path, 'r') as f:
    while True:
        line = f.readline()

        if(not line):
            break
        
        result = (1.0 - dq *(1.0/tq))
        d = random.random()

        if(d < result):
            continue

        c += 1

        if(c > dq):
            break

        data = json.loads(line)

        query = """INSERT INTO
                reddit_samples (
                    subreddit,
                    subreddit_id,
                    subreddit_type,
                    author,
                    body,
                    created_date,
                    created_utc,
                    retrieved_on,
                    id,
                    parent_id,
                    link_id,
                    score,
                    total_awards_received,
                    controversiality,
                    gilded,
                    collapsed_because_crowd_control,
                    collapsed_reason,
                    distinguished,
                    removal_reason,
                    author_created_utc,
                    author_fullname,
                    author_patreon_flair,
                    author_premium,
                    can_gild,
                    can_mod_post,
                    collapsed,
                    is_submitter,
                    "_edited",
                    locked,
                    quarantined,
                    no_follow,
                    send_replies,
                    stickied,
                    author_flair_text
                )
            VALUES
            (
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?,
                    ?
                );"""
        try: subreddit= data["subreddit"] 
        except (KeyError, IndexError):subreddit= None
        try: subreddit_id= data["subreddit_id"] 
        except (KeyError, IndexError):subreddit_id= None
        try: subreddit_type= data["subreddit_type"] 
        except (KeyError, IndexError):subreddit_type= None
        try: author= data["author"] 
        except (KeyError, IndexError):author= None
        try: body= data["body"] 
        except (KeyError, IndexError):body= None
        try: created_date= data["created_date"] 
        except (KeyError, IndexError):created_date= None
        try: created_utc= data["created_utc"] 
        except (KeyError, IndexError):created_utc= None
        try: retrieved_on= data["retrieved_on"] 
        except (KeyError, IndexError):retrieved_on= None
        try: id= data["id"] 
        except (KeyError, IndexError):id= None
        try: parent_id= data["parent_id"] 
        except (KeyError, IndexError):parent_id= None
        try: link_id= data["link_id"] 
        except (KeyError, IndexError):link_id= None
        try: score= data["score"] 
        except (KeyError, IndexError):score= None
        try: total_awards_received= data["total_awards_received"] 
        except (KeyError, IndexError):total_awards_received= None
        try: controversiality= data["controversiality"]
        except (KeyError, IndexError):controversiality= None
        try: gilded= data["gilded"] 
        except (KeyError, IndexError):gilded= None
        try: collapsed_because_crowd_control= data["collapsed_because_crowd_control"] 
        except (KeyError, IndexError):collapsed_because_crowd_control= None
        try: collapsed_reason= data["collapsed_reason"]
        except (KeyError, IndexError):collapsed_reason= None
        try: distinguished= data["distinguished"]
        except (KeyError, IndexError):distinguished= None
        try: removal_reason= data["removal_reason"] 
        except (KeyError, IndexError):removal_reason= None
        try: author_created_utc= data["author_created_utc"]
        except (KeyError, IndexError):author_created_utc= None
        try: author_fullname= data["author_fullname"]
        except (KeyError, IndexError):author_fullname= None
        try: author_patreon_flair= data["author_patreon_flair"]
        except (KeyError, IndexError):author_patreon_flair= None
        try: author_premium= data["author_premium"] 
        except (KeyError, IndexError):author_premium= None
        try: can_gild= data["can_gild"] 
        except (KeyError, IndexError):can_gild= None
        try: can_mod_post= data["can_mod_post"]
        except (KeyError, IndexError):can_mod_post= None
        try: collapsed= data["collapsed"] 
        except (KeyError, IndexError):collapsed= None
        try: is_submitter= data["is_submitter"] 
        except (KeyError, IndexError):is_submitter= None
        try: edited= data["_edited"] 
        except (KeyError, IndexError):edited= None
        try: locked= data["locked"] 
        except (KeyError, IndexError):locked= None
        try: quarantined= data["quarantined"] 
        except (KeyError, IndexError):quarantined= None
        try: no_follow= data["no_follow"]
        except (KeyError, IndexError):no_follow= None
        try: send_replies= data["send_replies"] 
        except (KeyError, IndexError):send_replies= None
        try: stickied= data["stickied"] 
        except (KeyError, IndexError):stickied= None
        try: author_flair_text= data["author_flair_text"]
        except (KeyError, IndexError):author_flair_text= None
        
        params = (subreddit,
                subreddit_id,
                subreddit_type,
                author,
                body,
                created_date,
                created_utc,
                retrieved_on,
                id,
                parent_id,
                link_id,
                score,
                total_awards_received,
                controversiality,
                gilded,
                collapsed_because_crowd_control,
                collapsed_reason,
                distinguished,
                removal_reason,
                author_created_utc,
                author_fullname,
                author_patreon_flair,
                author_premium,
                can_gild,
                can_mod_post,
                collapsed,
                is_submitter,
                edited,
                locked,
                quarantined,
                no_follow,
                send_replies,
                stickied,
                author_flair_text)

        count = cursor.execute(query, params)

print(c)

sqliteConnection.commit()
print("Records inserted successfully into SqliteDb_developers table", cursor.rowcount)
cursor.close()