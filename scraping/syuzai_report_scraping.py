from selenium import webdriver
import time
import pandas as pd
import re
from selenium.webdriver.common.by import By
#from datetime import datetime, date, timedelta
from selenium.webdriver.chrome.options import Options
import requests
import json

from webdriver_manager.chrome import ChromeDriverManager
import mysql
import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv(".env")

#functions-framework --target=syuzaibetu_hallnavi_scraping --signature-type=event --debug --port=8080
#functions-framework --target=syuzaibetu_hallnavi_scraping --port=8081 --signature-type=event
print('ライブラリの読み込み完了')
# def syuzaibetu_hallnavi_scraping(event,context):
#     global furture_syuzai_list_df_1,cnx
def removal_text(text):
    text = unicodedata.normalize("NFKC", text)
    text = text.translate(str.maketrans( '', '',string.punctuation  + '！'+ '　'+ ' '+'・'+'～' + '‐'))
    return text

def insert_data_bulk(df,cnx):
    insert_sql = """INSERT INTO hallnavi_gcp (都道府県, 日付, 曜日, 店舗名, 取材名, 媒体名, ランク) values (%s,%s,%s,%s,%s,%s,%s)"""
    cur = cnx.cursor()
    cur.executemany(insert_sql, df.values.tolist())
    print("Insert bulk data")

def post_line_text(message,token):
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization" : "Bearer "+ token}
    payload = {"message" :  message}
    post = requests.post(url ,headers = headers ,params=payload) 

def post_line_text_and_image(message,image_path,token):
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization" : "Bearer "+ token}
    payload = {"message" :  message}
    #imagesフォルダの中のgazo.jpg
    print('image_path',image_path)
    files = {"imageFile":open(image_path,'rb')}
    post = requests.post(url ,headers = headers ,params=payload,files=files) 


def insert_data_bulk(df,cnx):
    insert_sql = """INSERT INTO hallnavi_gcp (都道府県, 日付, 曜日, 店舗名, 取材名, 媒体名, ランク) 
    values (%s,%s,%s,%s,%s,%s,%s)"""
    cur = cnx.cursor()
    cur.executemany(insert_sql, df.values.tolist())
    print("Insert bulk data")


options = Options()
options.add_argument('--headless')
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--disable-features=NetworkService")
options.add_argument("--window-size=1920x1080")
options.add_argument("--disable-features=VizDisplayCompositor")
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
options.add_argument('--user-agent=' + UA)

browser = webdriver.Chrome(ChromeDriverManager().install(),options=options)#ChromeDriverManager().install() 
browser.implicitly_wait(10)
url_login = f"https://{os.getenv('SCRAPING_SYUZAI_DOMAIN')}/login_form_mail"
#admageを開く
browser.get(url_login)
browser.implicitly_wait(10)
# #id
# element = browser.find_element(By.NAME,"id")
# element.click()
# browser.implicitly_wait(10)
# element.send_keys(os.getenv('REPORT_SITE_ID'))

# # pw
# element = browser.find_element(By.NAME,"pass")
# element.click()
# browser.implicitly_wait(10)
# element.send_keys(os.getenv('REPORT_SITE_PW'))

# browser.implicitly_wait(10)
# element = browser.find_element(By.CLASS_NAME,"box_hole_view_report_input")
# element.click()
# browser.implicitly_wait(10)
url = f"https://{os.getenv('SCRAPING_SYUZAI_DOMAIN')}/select_area"
browser.get(url)
browser.implicitly_wait(10)
url = f"https://{os.getenv('SCRAPING_SYUZAI_DOMAIN')}/?area=kanto"
browser.get(url)
browser.implicitly_wait(10)
import datetime
tomorrow = datetime.date.today() + datetime.timedelta(days=1)
tomorrow_str = tomorrow.strftime("%m月%d日")
tomorrow_url = tomorrow.strftime("%Y-%m-%d")
today = datetime.date.today()

# todouhuken_number = 27
# prefectures = '大阪府'
# url = ff"https://{os.getenv('SCRAPING_SYUZAI_DOMAIN')}/osusume_list?ken={todouhuken_number}&ymd={tomorrow_url}"
# browser.get(url)
# browser.implicitly_wait(10)


#insert_data_bulk(preprocessingf_furture_syuzai_list_df)
#cnx.commit()
#post_line_text('大阪取材予定追加おわり','e85117mYEFu8efTmrXdR0nSRUgQJRxxVN0CMazT1efV')
furture_syuzai_list_df = pd.DataFrame(index=[], columns=['都道府県','日付','店舗名','取材名','媒体名','ランク'])
elements = browser.find_elements(By.CLASS_NAME,"mgn_serch_list_bottom")
for i in range(14,50):
    browser.find_element(By.CLASS_NAME,"head_change_main").click()
    time.sleep(1)
    if 'プレミアム会員登録' == browser.find_element(By.CLASS_NAME,"menu_child").text:
        browser.implicitly_wait(10)
        url_login = f"https://{os.getenv('SCRAPING_SYUZAI_DOMAIN')}/login_form_mail"
        #admageを開く
        browser.get(url_login)
        browser.implicitly_wait(10)
        # id
        element = browser.find_element(By.NAME,"id")
        element.click()
        browser.implicitly_wait(10)
        element.send_keys(os.getenv('REPORT_SITE_ID'))

        # pw
        element = browser.find_element(By.NAME,"pass")
        element.click()
        browser.implicitly_wait(10)
        element.send_keys(os.getenv('REPORT_SITE_PW'))

        browser.implicitly_wait(10)
        element = browser.find_element(By.CLASS_NAME,"box_hole_view_report_input")
        element.click()
        browser.implicitly_wait(10)
        url = f"https://{os.getenv('SCRAPING_SYUZAI_DOMAIN')}/select_area"
        browser.get(url)
        browser.implicitly_wait(10)
        url = f"https://{os.getenv('SCRAPING_SYUZAI_DOMAIN')}/?area=kanto"
        browser.get(url)
        browser.implicitly_wait(10)
    else:
        pass
    try:
        elements = browser.find_elements(By.CLASS_NAME,"mgn_serch_list_bottom")
        baitai_name = elements[i].text.split(' ')[0]
        baitai_name = baitai_name.replace('パチマガスロマガじゃ…','パチマガスロマガ').replace('パチンコ店長のホール…','パチンコ店長のホール攻略')
        print(baitai_name)
        elements[i].click()
        for syuzai_tenpo_data in browser.find_elements(By.CLASS_NAME,"osbox"):
            tenpo_name = syuzai_tenpo_data.find_element(By.CLASS_NAME,"oslh2").text
            #print(tenpo_name.text)
            syuzai_date = syuzai_tenpo_data.find_element(By.CLASS_NAME,"oslmd").text
            rank_and_syuzai_name = syuzai_tenpo_data.find_element(By.CLASS_NAME,"list_event_name").text
            syuzai_rank = rank_and_syuzai_name.split('\n')[0]
            syuzai_name = rank_and_syuzai_name.split('\n')[1]
            prefectures = syuzai_tenpo_data.find_elements(By.CLASS_NAME,"oslha")[0].text
            #print(baitai_name,syuzai_date ,syuzai_rank,syuzai_name,prefectures)#prefectures
            record = pd.Series([prefectures,syuzai_date, tenpo_name,syuzai_name,baitai_name,syuzai_rank], index=furture_syuzai_list_df.columns)
            furture_syuzai_list_df = furture_syuzai_list_df.append(record, ignore_index=True)
            #print(record)
            #break
            browser.implicitly_wait(10)
        # time.sleep(1)
        #break
        #break
    except:
        break
    # if i > 13:
    #     break


browser.quit()

pattern = '東京都|北海道|(京都|大阪)府|.{2,3}県'
# 都道府県を抽出する
furture_syuzai_list_df = furture_syuzai_list_df[furture_syuzai_list_df['都道府県'] != '']
# furture_syuzai_list_df['都道府県']=furture_syuzai_list_df['都道府県'].apply(lambda x:re.match(pattern,x).group())
prefectures_list = []
for adress in furture_syuzai_list_df['都道府県']:
    adress = adress.split(']')[-1]
    try:
        #print(re.match(pattern,adress).group())
        prefectures_list.append(re.match(pattern,adress).group())
    except:
        prefectures_list.append('情報なし')
furture_syuzai_list_df['都道府県'] = prefectures_list
furture_syuzai_list_df_1 = furture_syuzai_list_df
furture_syuzai_list_df_1 = pd.concat([furture_syuzai_list_df_1, furture_syuzai_list_df_1['日付'].str.split('(', expand=True)], axis=1).drop('日付', axis=1)
furture_syuzai_list_df_1.rename(columns={0: '日付', 1: '曜日'}, inplace=True)
furture_syuzai_list_df_1['曜日'] = furture_syuzai_list_df_1['曜日'].map(lambda x:x.replace(')',''))
furture_syuzai_list_df_1['日付'] = pd.to_datetime(furture_syuzai_list_df_1['日付'])
furture_syuzai_list_df_1 = furture_syuzai_list_df_1 [['都道府県','日付','曜日',	'店舗名','取材名','媒体名','ランク']]

#### Create dataframe from resultant table ####
cnx = mysql.connector.connect(
                        user = os.getenv('DB_USER_NAME'),
                        password=os.getenv('DB_PASSWORD'), 
                        host=os.getenv('DB_HOST'), 
                        port='3306',
                        database=os.getenv('DB_NAME'))

cursor = cnx.cursor()
sql = "SELECT * FROM syuzai_report_table"
cursor.execute(sql)
#cols = [col[0] for col in cursor.description]
sql_syuzai_report_all_df = pd.DataFrame(cursor.fetchall(),columns = ['都道府県','日付','店舗名','取材名','媒体名','ランク'])
#df
# cursor = cnx.cursor()
# # #### Connetion Established ####
# # #### Execute query ####
# query1 = ("select * from hallnavi_gcp")
# cursor.execute(query1)
# #### Create dataframe from resultant table ####

sql_syuzai_report_all_df
concat_df = pd.concat([sql_syuzai_report_all_df,furture_syuzai_list_df_1])
concat_df['日付'] = pd.to_datetime(concat_df['日付'])
concat_df = concat_df[~concat_df.duplicated(keep=False)]
insert_data_bulk(concat_df,cnx)
cnx.commit()

post_line_text(f'{len(concat_df)}件の関東取材予定追加おわり',os.getenv('LINE_TOKEN'))
