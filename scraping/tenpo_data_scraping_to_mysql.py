import pandas as pd
import datetime
import time
import unicodedata
import string
import requests
import mysql.connector
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# .env ファイルをロードして環境変数へ反映
from dotenv import load_dotenv
load_dotenv('.env')
# 環境変数を参照

def removal_text(text):
    text = unicodedata.normalize("NFKC", text)
    text = text.translate(str.maketrans( '', '',string.punctuation  + '！'+ '　'+ ' '+'・'+'～' + '‐'))
    return text

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
    insert_sql = """INSERT INTO test_table (店舗名, 日付, Nのつく日, 都道府県, 機種名, 台番号, G数, 差枚, BB, RB,ART, BB確率, RB確率, ART確率, 合成確率) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    cur = cnx.cursor()
    cur.executemany(insert_sql, df.values.tolist())
    cnx.commit()
    print("Insert bulk data")

options = Options()
options.add_argument("--headless")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")
# options.add_argument("--disable-gpu")
# options.add_argument("--disable-features=NetworkService")
# options.add_argument("--window-size=1920x1080")
# options.add_argument("--disable-features=VizDisplayCompositor")
# UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
# options.add_argument('--user-agent=' + UA)
# mobile_emulation = { "deviceName": "Galaxy S5" }
# options.add_experimental_option("mobileEmulation", mobile_emulation)

prefecture = '神奈川県'

line_token = os.getenv('LINE_TOKEN')
#print(line_token)
post_line_text(f'{prefecture}MYSQL追加処理を開始します',line_token)

try:
    cols = ['機種名', '台番号', 'G数', '差枚', 'BB', 'RB', 'ART', 'BB確率', 'RB確率', 'ART確率','合成確率','店舗名']
    ichiran_all_tennpo_df = pd.DataFrame(index=[], columns=cols)
    yesterday = datetime.date.today() + datetime.timedelta(days=-1)
    browser = webdriver.Chrome(ChromeDriverManager().install(),options=options)
    url = f'https://{os.getenv("SCRAPING_DOMAIN")}/%E3%83%9B%E3%83%BC%E3%83%AB%E3%83%87%E3%83%BC%E3%82%BF/{prefecture}/'
    browser.get(url)
    html = browser.page_source.encode('utf-8')
    soup = BeautifulSoup(html, 'lxml')
    tenpo_ichiran_df = pd.read_html(html)[-1]
    #print(tenpo_ichiran_df['ホール名'])

    i = 0
    for tenpo_name in tenpo_ichiran_df['ホール名'] :#tenpo_ichiran_df['ホール名']
        try:
            print(tenpo_name)
            url = f'https://{os.getenv("SCRAPING_DOMAIN")}/{yesterday.strftime("%Y-%m-%d")}-{tenpo_name}'
            browser.get(url)
            html = browser.page_source.encode('utf-8')
            dfs = pd.read_html(html)
            #display(tenpo_df)
            time.sleep(1)
            for df in  dfs:
            #print(df.columns)
                if '機種名' in list(df.columns):
                    ichiran_df = df
                    ichiran_df['日付'] = yesterday.strftime('%Y-%m-%d')
                    ichiran_df['店舗名'] = tenpo_name
                    print(tenpo_name)
                    ichiran_df['Nのつく日'] = yesterday.strftime('%d')[-1]
                    ichiran_df['都道府県'] = prefecture 
                    ichiran_df['機種名'] = ichiran_df['機種名'].map(removal_text)
                    ichiran_all_tennpo_df =  pd.concat([ichiran_all_tennpo_df, ichiran_df])
                    break
                
        except:
            time.sleep(1)
            continue
        
        i += 1
        if i > 3:
            break
    
    browser.quit()
    
    cols = ichiran_all_tennpo_df.columns.tolist()
    cols = cols[-4:] + cols[:-4]
    ichiran_all_tennpo_df = ichiran_all_tennpo_df[cols]  #    OR    df = df.ix[:, cols]
    ichiran_all_tennpo_df['ART']= ichiran_all_tennpo_df['ART'].fillna(0)
    ichiran_all_tennpo_df['BB']= ichiran_all_tennpo_df['BB'].fillna(0)
    ichiran_all_tennpo_df['RB']= ichiran_all_tennpo_df['RB'].fillna(0)
    ichiran_all_tennpo_df['差枚']= ichiran_all_tennpo_df['差枚'].fillna(0)
    ichiran_all_tennpo_df['G数']= ichiran_all_tennpo_df['G数'].fillna(0)
    ichiran_all_tennpo_df = ichiran_all_tennpo_df.fillna('')
    #print(ichiran_all_tennpo_df.iloc[:5])
    
    cnx = mysql.connector.connect(
                            user = os.getenv('DB_USER_NAME'),
                            password=os.getenv('DB_PASSWORD'), 
                            host=os.getenv('DB_HOST'), 
                            port='3306',
                            database=os.getenv('DB_NAME'))
    cursor = cnx.cursor()
    insert_data_bulk(ichiran_all_tennpo_df,cnx)
    
    tenpo_name_number = len(ichiran_all_tennpo_df['店舗名'].unique())
    post_line_text(f'{prefecture}{tenpo_name_number}件のSQL追加処理に成功しました',line_token)
    
except Exception as e:
    print(e)
    post_line_text(f'{prefecture}処理失敗{e}',line_token)

finally:
    print('終了')
