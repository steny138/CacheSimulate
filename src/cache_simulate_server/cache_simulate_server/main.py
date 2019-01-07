import schedule
import time
import datetime
import requests
from pymongo import MongoClient

client = MongoClient('mongodb://root:1qaz2wsx@127.0.0.1:27017/admin')
db = client.admin

def job():
    dt = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    # 找出全部logs
    process_logs = db.logs.find()

    slices = {}
    for process_log in process_logs:
        key = process_log['cache_key']
        val = process_log['value']
         
        # 清空 mongodb
        db.logs.find_one_and_delete({'_id': process_log['_id']})

        if slices.get(key):
            slices.get(key)['count'] += 1
        else:
            slices[key] = {
                'cache_key': key,
                'cache_value': val,
                'count' : 1
            }

    for k, v in slices.items():
        # 找到時間輪
        timewheel = db.timewheel.find_one({'cache_key':k})
        if not timewheel:
            timewheel = {'cache_key': k, 'cache_value':v['cache_value'], 'timeslices': []}
            db.timewheel.insert_one(timewheel)
    
        timewheel['cache_value'] = v['cache_value']

        # 收集資訊 產生時間片
        timewheel['timeslices'].append({'datetime': dt, 'count': v['count']})
        
        # 將資料更新到時間輪中
        db.timewheel.find_one_and_replace({'cache_key':k}, timewheel)
    
    print("將資料節轉到時間片中")

def job2():
    # 結轉時間輪的資料
    timewheels = db.timewheel.find()

    temp = []
    for timewheel in timewheels:
        slices = timewheel['timeslices']
        if len(slices) < 10:
            continue
        
        # 結轉次數並把過期時間片移除
        total = sum(c['count'] for c in slices)

        timewheel['total'] = total

        slices.sort(key=lambda x: datetime.datetime.strptime(x['datetime'], "%Y/%m/%d %H:%M:%S"), reverse=True)

        timewheel['timeslices'] = slices[:10]

        # 將資料更新到時間輪中
        db.timewheel.find_one_and_replace({'_id':timewheel['_id']}, timewheel)

        temp.append(timewheel)

    print("結轉到時間輪")

    # 找出熱點資訊
    sort_timewheels = [x for x in temp if len(x['timeslices']) >= 10]
    
    sort_timewheels = sorted(sort_timewheels, key=lambda x: x['total'], reverse=True)
    
    post_data = []
    for sort_timewheel in sort_timewheels[:5]:
        post_data.append({'cache_key': sort_timewheel['cache_key'], 'cache_value': sort_timewheel['cache_value']})

    # 投放熱點資訊
    # POST '127.0.0.1:5000/hotkey'
    r = requests.post('http://localhost:5000/hotkey', json = {'caches': post_data})

    print("投放熱點")

schedule.every(10).seconds.do(job)
schedule.every().minutes.do(job2)

while 1:
    schedule.run_pending()
    time.sleep(1)