import random

import requests

import schedule

import time

# 手動加權
county_list = ["台北市","新北市","台北市","新北市","台北市","新北市","台北市","新北市",
"基隆市","新竹市","新竹市",
"台中市","台中市","台中市","高雄市","高雄市","高雄市",
"桃園市","台南市","台南市"]

districs = [
    {"Country":"台北市","Districts":["中正區","大同區","中山區","松山區","大安區","信義區","內湖區","南港區","文山區"]},
    {"Country":"新北市","Districts":["板橋區","新店區","永和區","中和區","三重區","新莊區","蘆洲區","淡水區"]},
    {"Country":"基隆市","Districts":["仁愛區","信義區","中正區","中山區"]},
    {"Country":"宜蘭縣","Districts":["宜蘭市","頭城鎮","礁溪鄉","壯圍鄉","員山鄉","羅東鎮"]},
    {"Country":"新竹市","Districts":["新竹市","東區","北區","香山區"]},
    {"Country":"新竹縣","Districts":["竹北市","湖口鄉","新豐鄉","新埔鎮","關西鎮","芎林鄉"]},
    {"Country":"桃園市","Districts":["中壢區","平鎮區","龍潭區","楊梅區","新屋區","觀音區"]},
    {"Country":"苗栗縣","Districts":["竹南鎮","頭份市","三灣鄉","南庄鄉","獅潭鄉","後龍鎮","泰安鄉","銅鑼鄉","三義鄉","西湖鄉","卓蘭鎮"]},
    {"Country":"台中市","Districts":["中區","東區","南區","西區","北區","北屯區","西屯區","石岡區","東勢區","梧棲區","清水區","大甲區","外埔區","大安區"]},
    {"Country":"彰化縣","Districts":["彰化市","芬園鄉","花壇鄉","秀水鄉","鹿港鎮","福興鄉","溪湖鎮","大村鄉","大城鄉","芳苑鄉","二水鄉"]},
    {"Country":"南投縣","Districts":["南投市","中寮鄉","草屯鎮","國姓鄉","埔里鎮","仁愛鄉"]},
    {"Country":"嘉義市","Districts":["嘉義市","東區","西區"]},
    {"Country":"嘉義縣","Districts":["水上鄉","鹿草鄉","太保市","朴子市","新港鄉","民雄鄉"]},
    {"Country":"雲林縣","Districts":["斗南鎮","大埤鄉","虎尾鎮","土庫鎮","褒忠鄉","東勢鄉","臺西鄉","崙背鄉","麥寮鄉","斗六市"]},
    {"Country":"台南市","Districts":["中西區","東區","南區","西區","北區","安平區","安南區","永康區","歸仁區","新化區","仁德區","麻豆區","將軍區","學甲區","北門區","新營區","善化區","新市區"]},
    {"Country":"高雄市","Districts":["新興區","前金區","苓雅區","鹽埕區","鼓山區","旗津區","前鎮區","三民區","楠梓區","小港區","左營區","仁武區","大社區","岡山區"]},
    {"Country":"屏東縣","Districts":["屏東市","三地門鄉","霧台鄉","瑪家鄉","九如鄉"]},
    {"Country":"台東縣","Districts":["臺東市","綠島鄉","蘭嶼鄉","延平鄉","卑南鄉","大武鄉"]},
    {"Country":"花蓮縣","Districts":["花蓮市","玉里鎮","卓溪鄉","富里鄉"]}]

purpose_list = ["住宅","住宅","住宅","住宅","住宅", "住宅", 
"住宅", "住宅", "店面", "店面", "店面", "店面",
"辦公室", "廠房", "土地", "倉庫", "其他"]

price_list = ["0", "400", "800", "1200", "2000", "3000"]

def main():
    print("隨機送出request 10次")
    # 隨機送出request
    for i in range(0, 10 , 1):  
        # 取得縣市
        county = random.choice(county_list)

        # 取得區域
        district = [random.choice(x['Districts']) for x in districs if x['Country'] == county][0]

        # 取得用途
        purpose = random.choice(purpose_list)

        # 取得價格
        price_l = random.choice(price_list)

        price_h = random.choice(price_list)

        if int(price_h) < int(price_l):
            price_h = price_l

        payload = {'county': county, 
        'district': district, 
        'purpose': purpose, 
        'pricel': price_l, 
        'priceh': price_h}

        r = requests.get('http://localhost:5000/', params=payload)
        
        print(r.url)

    # while True:
    #無窮迴圈起手式  



if __name__ == '__main__':    
    schedule.every(5).seconds.do(main)

    while 1:
        schedule.run_pending()
        time.sleep(1)
