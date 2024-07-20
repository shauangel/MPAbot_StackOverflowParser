from pymongo import MongoClient
from pytz import timezone
from datetime import datetime as dt
import json

# container
client = MongoClient("mongodb://so-parser-mongo:27017/so-parser_db")
# test_client = MongoClient("mongodb://localhost:50002/")
# specify collections
DB = client['SOService']
POSTS_COLLECTION = DB['Posts']

TEST_DATA = DB['TestData']


# get current time and convert to TW timezone
def get_curr_time():
    dt_format = "%Y-%m-%d %H:%M:%S %Z%z"
    now_utc = dt.now(timezone('UTC'))
    now_tw = now_utc.astimezone(timezone('Asia/Taipei'))
    return now_tw.strftime(dt_format)


# query multiple posts in post cache collection by question id
def query_post_by_id(id_list):
    query = {"question.id": {"$in": id_list}}
    cursor = POSTS_COLLECTION.find(query)
    # remove object id
    result = []
    for d in cursor:
        d.pop("_id")
        result.append(d)
    # result = [d for d in cursor]
    print(result)
    return result


# insert multiple posts into post cache collection
def insert_posts(data_list):
    # record insert time
    time = get_curr_time()
    for d in data_list:
        d["saved_time"] = time
    # insert post data
    result = POSTS_COLLECTION.insert_many(data_list)
    return result


# delete multiple posts from cache according to question ids
def delete_posts_cache_by_id(id_list):
    try:
        query = {"question.id": {"$in": id_list}}
        del_result = TEST_DATA.delete_many(query)
        print(del_result)
    except Exception as e:
        print("Error deleting post cache...\n" + e.__class__.__name__ + ": " + e.args[0])


# auto data maintenance
def cache_maintenance():
    return 0


if __name__ == "__main__":
    print("Stack Overflow DB Manager")


