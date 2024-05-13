from pymongo import MongoClient
from pytz import timezone
from datetime import datetime as dt

# testing database
client = MongoClient("mongodb+srv://psabot:BmueEwQFrYx3IUBk@stackoverflow.b2tyvk9.mongodb.net/")

# container
# client = MongoClient("mongo:27017")

# specify collections
DB = client['SOService']
POSTS_COLLECTION = DB['Posts']
POSTS_CACHE_COLLECTION = DB['PostsCache']

TEST_DATA = DB['TestData']


# get current time and convert to TW timezone
def get_curr_time():
    dt_format = "%Y-%m-%d %H:%M:%S %Z%z"
    now_utc = dt.now(timezone('UTC'))
    now_tw = now_utc.astimezone(timezone('Asia/Taipei'))
    return now_tw.strftime(dt_format)


# query multiple posts in post cache collection by question id
def query_post_cache_by_id(id_list):
    query = {"question.id": {"$in": id_list}}
    cursor = TEST_DATA.find(query)
    # cursor = POSTS_CACHE_COLLECTION.find(query)
    result = [d for d in cursor]
    return result


# insert multiple posts into post cache collection
def insert_posts_cache(data_list):
    # record insert time
    time = get_curr_time()
    for d in data_list:
        d["date"] = time
    # insert post data
    result = POSTS_CACHE_COLLECTION.insert_many(data_list)
    print(result)


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
    # test_data = p.tester()
    # insert_posts_cache(test_data)
    test_find = [75017173, 21956683]
    # delete_posts_cache(test_del)
    r = query_post_cache_by_id(test_find)
    print(len(r))
