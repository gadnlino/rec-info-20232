import json
import sqlite3
import random

file_path = 'C:\\Users\\guiav\\Source_Code\\repos\\rec-info-20232\\article\\data\\news\\signalmedia-1m.jsonl\\sample-1M.jsonl'

sqliteConnection = sqlite3.connect('C:\\Users\\guiav\\Source_Code\\repos\\rec-info-20232\\article\\data\\data-sqlite')
cursor = sqliteConnection.cursor()
print("Successfully Connected to SQLite")

tq = 1_000_000
dq = 200

c = 0

related_news_ids = [
    '1478bf7b-1c23-4235-9ed2-b8c287fc952c',
    '4e74bbed-b449-48a8-a71c-f70499105289',
    '4bc04c2f-2d01-42d5-8311-e4005950d20f',
    'e2f6d043-d1b1-45d8-ae5e-34d03a081b18',
    'ef756748-9863-44d6-8cfc-66cbf0ccd975',
    'be94f275-223c-46bd-8efd-fafa03872368',
    '011e98e2-0434-4004-b020-7a4a81e12d68',
    '9c2abfde-02c5-4342-8a24-7c929090a6f8',
    '17e7c861-f3cf-49d3-bf93-4daf4a99324c',
    '86ffe840-0a6b-4e7d-9490-e24636a3a214',
    '35de6aea-82a0-41a8-9af8-38773e1dfc2c',
    '0e4f366b-0ecb-415d-bfc4-17494d5a4c58',
    '0429b914-907a-4d79-aed8-5e2a7ebaa230',
    '92ae56ba-2a40-46e7-8788-f5bf9a9dfb56',
    '62821356-38aa-4ed6-90d8-1c32a2e99a8e',
    '0b3bea50-3a2c-4d07-953e-45aca9988634',
    '43fcbb87-a47a-45fa-a306-a83324ac9bc9',
    'f853bd19-8f5b-468d-a261-a2cb9c7407bc',
    '68047331-25e1-4af5-974b-766f1338bef0',
    '9ce6dea5-1d7e-4648-bcc4-c53d3d4e4558',
    'c24983f3-70bc-4e1e-b1ab-75d559adc338'
]

with open(file_path, 'r') as f:
    while True:
        line = f.readline()

        if(not line):
            break
        
        data = json.loads(line)

        insert = random.random() >= dq * (1.0/tq)

        if(data['id'] in related_news_ids):
            insert = True
        else:
            c += 1

            insert = insert and c < dq

        if(insert):
            query = """INSERT INTO news_samples
                    (id, content, title, "media-type", "source", published)
                    VALUES(?, ?, ?, ?, ?, ?);"""
            
            params = (data['id'], data['content'], data['title'], data['media-type'], data['source'], data['published'])

            cursor.execute(query, params)

sqliteConnection.commit()
print("Records inserted successfully into SqliteDb_developers table ", cursor.rowcount)
cursor.close()