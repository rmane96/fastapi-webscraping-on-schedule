import datetime

# convert uuid1 time to readable datetime
def uuid_to_datetime(time:int):
    return datetime.datetime(1582, 10, 15) + datetime.timedelta(microseconds=time//10)
