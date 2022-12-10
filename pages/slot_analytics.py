
import datetime
import os
import plotly.express as px
import streamlit as st
import mysql.connector
import pandas as pd
import base64
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(layout="wide")
st.title("ポートフォリオ用サイト(データ分析）")
st.write(os.getenv('USER_NAME'))
yesterday = datetime.date.today() + datetime.timedelta(days=-2)
cnx = mysql.connector.connect(
                            user = os.getenv('USER_NAME'),
                            password=os.getenv('PASSWORD'), 
                            host=os.getenv('DB_HOST'), 
                            port='3306',
                            database=os.getenv('DB_NAME'))
#cnx.close()
cursor = cnx.cursor()
kisyu_name = ''

cursor.execute(f"""
SELECT * 
FROM {os.getenv('DB_NAME')}.test_table
WHERE (機種名 LIKE "%{kisyu_name}%") 
AND 日付 = '{yesterday.strftime('%Y-%m-%d')} 00:00:00' 
""")

#WHERE (店舗名 LIKE "%%") AND (日付 BETWEEN "{start_day}" AND "{last_day}") AND (機種名 LIKE "%{kisyu_name}%") 
cols = [col[0] for col in cursor.description]
all_tenpo__df = pd.DataFrame(cursor.fetchall(),columns = cols)
st.write(all_tenpo__df)

st.sidebar.title('SLOT_DB_analytics')
st.sidebar.title('複数店舗データ比較・検索用')

st.title('※検索データが大きすぎると固まるため必ず都道府県か店舗名を一つ以上指定してください')
@st.cache(allow_output_mutation=True)
def tenpo_name_list(sql):
    cnx = mysql.connector.connect(
                            user = os.getenv('USER_NAME'),
                            password=os.getenv('PASSWORD'), 
                            host=os.getenv('DB_HOST'), 
                            port='3306',
                            database=os.getenv('DB_NAME'))
    # cnx = mysql.connector.connect(user='root', 
    #                           password='6tjc5306',
    #                         host='34.136.72.129',
    #                         port='3306',
    #                         database='{st.secrets.db_credentials.database}')
    # #cnx.close()
    cursor = cnx.cursor()
    cursor.execute(sql)
    cols = [col[0] for col in cursor.description]
    df = pd.DataFrame(cursor.fetchall(),columns = cols)
    return df

yesterday = datetime.datetime.now() - datetime.timedelta(days = 2)
#yesterday = datetime.datetime(2022, 10, 10)
str_yesterday = yesterday.strftime("%Y-%m-%d")

sql = f"""
SELECT 店舗名,都道府県
FROM {os.getenv('DB_NAME')}.test_table
WHERE 日付 BETWEEN '{str_yesterday} 00:00:00' AND '{str_yesterday} 23:59:59'
"""

#st.write(sql)
df = tenpo_name_list(sql)
#st.write(df)

#  #sys.sys_config
# #rows = cursor.fetchall()
# #for row in rows:
#     # print(row)
#     # break

#サイドバー部分
st.sidebar.header('検索候補') 
sql =  f'SELECT * FROM {os.getenv("DB_NAME")}.test_table WHERE '

#tenpo_name_kouho = st.sidebar.selectbox('店舗名候補一覧',list(df['店舗名'].unique()))
tenpo_name= st.sidebar.text_input('店舗名指定(一部を含む可):', 'マルハン')
#tenpo_name = st.sidebar.selectbox('どの店舗を見ますか？',tuple(df['店舗名'].unique()))
# tenpo_name= st.sidebar.text_input('店舗名指定(~を含む):', '')

if len(tenpo_name) != 0:
    sql +=  f' 店舗名 LIKE "%{tenpo_name}%"'
else:
    pass

#st.sidebar.write('店舗名指定:', tenpo_name)
kisyu_name= st.sidebar.text_input('機種名指定(一部を含む可):', '')

if len(tenpo_name) == 0:
    if len(kisyu_name) == 0:
        pass
    else:
        sql += f' (機種名 LIKE "%{kisyu_name}%")'
else:
    sql += f' AND (機種名 LIKE "%{kisyu_name}%") '

select_date , last_day = st.sidebar.date_input("取得するデータの範囲を指定してください",value=(yesterday,yesterday))
str_select_date  = select_date.strftime('%Y年%m月%d日')
str_last_day  = last_day.strftime('%Y年%m月%d日')
st.sidebar.write('日付範囲:', str_select_date ,'〜', str_last_day)
sql += f' '


# date_list = []
# for i in range(1,27):
#     date = datetime.datetime.now() - datetime.timedelta(days = i)
#     str_date = date.strftime("%Y-%m-%d")
#     print(str_date)
#     date_list.append(str_date)

# print(date_list)
# select_date = st.sidebar.selectbox('取得日を指定する',tuple(date_list))

if len(tenpo_name) == 0 & len(kisyu_name) == 0:
    sql += f' (日付 BETWEEN "{select_date}" AND "{last_day}")'
else:
    sql += f' AND (日付 BETWEEN "{select_date}" AND "{last_day}")'


#st.sidebar.write('都道府県指定:(複数指定可(東京都、神奈川県など)')
todouhuken_list = st.sidebar.multiselect('都道府県指定:',list(df['都道府県'].unique()),['神奈川県'])
#sql +=  ' AND (都道府県 IS NULL) '#f'AND (都道府県 LIKE "%{todouhuken}%") '

if len(todouhuken_list) != 0:
    sql += 'AND ('
    for i, prefecture in enumerate(todouhuken_list):
        print(i)
        if i != len(todouhuken_list) - 1 :
            sql +=  f'( 都道府県 = "{prefecture}" ) OR '
        else:
            sql +=  f'( 都道府県 = "{prefecture}" )'
    sql += ')' 
else:
    pass

day_of_number_list = st.sidebar.multiselect('Nのつく日指定:',[0,1,2,3,4,5,6,7,8,9],[])#,disabled=True
if len(day_of_number_list) != 0:
    sql += 'AND ('
    for i, day_of_number in enumerate(day_of_number_list):
        print(i)
        if i != len(day_of_number_list) - 1 :
            sql +=  f'(Nの日 = {day_of_number }) OR '
        else:
            sql +=  f'(Nの日 = {day_of_number })'
    sql += ')'
else:
    pass


day_of_week_dict = {'日':1,'月':2, '火':3, '水':4, '木':5,'金':6,'土':7}
day_of_week = st.sidebar.multiselect('曜日指定',['月', '火', '水', '木','金','土','日'],[])#,disabled=True

if len(day_of_week) != 0:
    sql += 'AND ('
    for i, day_of_week_of_number in enumerate(day_of_week):
        print(i)
        if i != len(day_of_week) - 1 :
            sql +=  f'(DAYOFWEEK(日付) = "{day_of_week_dict[day_of_week_of_number]}") OR '
        else:
            sql +=  f'(DAYOFWEEK(日付) = "{day_of_week_dict[day_of_week_of_number]}")'
    sql += ')'
else:
    pass


st.title('検索結果')
#@st.cache(suppress_st_warning=True)
print('sqlは',sql)
@st.cache(allow_output_mutation=True)
def query_database(sql):
    print('SQLは',sql,'です')
    cursor.execute(sql)
    cols = [col[0] for col in cursor.description]
    extract_df = pd.DataFrame(cursor.fetchall(),columns = cols)
    extract_df['日付'] = extract_df['日付'].astype(str)
    extract_df['nの日'] =  extract_df['日付'].map(convert_add_n_day)
    extract_df['日付'] = pd.to_datetime(extract_df['日付'])
    date = extract_df['日付'].dt.strftime('%a')
    extract_df['曜日'] = date
    extract_df = extract_df.sort_values(['日付','店舗名','台番号'])
    #st.dataframe(extract_df, width=2500, height=500)
    return extract_df

def convert_add_n_day(date_string):
    date_string = str(date_string).replace(' 0:00:00','')
    n_day_string = str(date_string)[-1]
    return n_day_string

def encoding_text(text):
    bytes_emoji = text.encode('shift-jis', errors='ignore')
    result = bytes_emoji.decode('shift-jis', errors='ignore')
    return text


#@st.cache(allow_output_mutation=True)
def output_graph_whole_anaytics(extract_df,todoufuken='',tenpo_name='',kisyu_name='',select_date=datetime.date(2022, 4, 1),last_day=datetime.date(2022, 6, 30)):
    #全体分析関数
    reset_index_bariety_pulledout_all_day_df = extract_df
    reset_index_bariety_pulledout_all_day_df['日付'] = reset_index_bariety_pulledout_all_day_df['日付'].astype(str)
    reset_index_bariety_pulledout_all_day_df['nの日'] =  reset_index_bariety_pulledout_all_day_df['日付'].map(convert_add_n_day)
    n_day_groupued_all_day_df = reset_index_bariety_pulledout_all_day_df.groupby(['nの日']).sum().reset_index()
    n_day_groupued_all_day_df['台数'] = list(reset_index_bariety_pulledout_all_day_df.groupby(['nの日']).size())
    print(n_day_groupued_all_day_df)
    n_day_groupued_all_day_df['平均差枚'] = n_day_groupued_all_day_df['差枚'] / n_day_groupued_all_day_df['台数']
    #n_day_groupued_all_day_df = n_day_groupued_all_day_df.drop(['日付','機種名','BB確率','RB確率','合成確率','ART','ART確率'],axis=1)
    n_day_groupued_all_day_df['平均G数'] = n_day_groupued_all_day_df['G数'] / n_day_groupued_all_day_df['台数'] 
    n_day_groupued_all_day_df['平均G数'] = n_day_groupued_all_day_df['平均G数'].astype(int)
    n_day_groupued_all_day_df['平均差枚'] = n_day_groupued_all_day_df['平均差枚'].astype(int)
    print(n_day_groupued_all_day_df)

    st.title('nの日別総差枚データ')
    st.dataframe(n_day_groupued_all_day_df, width=2500, height=400)
    n_day_groupued_all_day_df['差枚'] = n_day_groupued_all_day_df['差枚'].astype(int)
    n_day_groupued_all_day_df['nの日'] = n_day_groupued_all_day_df['nの日'].astype(int)
    n_day_samai_df = n_day_groupued_all_day_df.drop(['台番号','G数','BB','RB','台数','平均G数','nの日','平均差枚'],axis=1)
    st.title('nの日別グラフ')
    st.bar_chart(n_day_samai_df)
    return  n_day_groupued_all_day_df

    fig = px.bar(n_day_groupued_all_day_df, x='nの日', y='差枚', title=f"{tenpo_name} nの日毎の総差枚(累計)")
    st.plotly_chart(fig, use_container_width=True)

    # fig = px.bar(reset_index_bariety_pulledout_all_day_df.groupby(['nの日','日付']).sum().reset_index(), x='nの日', y='差枚', title=f"{tenpo_name} nの日毎の総差枚(日別)")
    # return fig.show()
    # st.plotly_chart(fig, use_container_width=True)
    
if st.sidebar.button('検索'):
    st.write(f'{tenpo_name} {kisyu_name} {select_date}で検索しました')
    st.write(sql)
    extract_df = query_database(sql)
    
    if len(extract_df) == 0:
        st.write('データがありません。検索条件を変更したください')
        st.stop()
        
    extract_df['機種名'] = extract_df['機種名'].map(encoding_text)
    extract_df = extract_df.drop(['台番号'],axis=1)
    tenpobetsu_groupby_df = extract_df.groupby('店舗名').sum()
    tenpobetsu_groupby_df['台数'] = extract_df.groupby('店舗名').size()
    tenpobetsu_groupby_df = tenpobetsu_groupby_df.reset_index()
    st.write(tenpobetsu_groupby_df)
    tenpobetsu_groupby_df['平均差枚'] = tenpobetsu_groupby_df['差枚'] / tenpobetsu_groupby_df['台数']
    #tenpobetsu_groupby_df = tenpobetsu_groupby_df.drop(['日付','機種名','BB確率','RB確率','合成確率','ART','ART確率'],axis=1)
    tenpobetsu_groupby_df['平均G数'] = tenpobetsu_groupby_df['G数'] / tenpobetsu_groupby_df['台数'] 
    tenpobetsu_groupby_df['平均G数'] = tenpobetsu_groupby_df['平均G数'].astype(int)
    tenpobetsu_groupby_df['平均差枚'] = tenpobetsu_groupby_df['平均差枚'].astype(int)
    st.title('店舗別一覧概要データ')
    st.write(tenpobetsu_groupby_df)

    st.title('日別平均差枚順グラフ')
    # Here we use a column with categorical data
    fig = px.histogram(tenpobetsu_groupby_df,x="平均差枚", y="店舗名", text_auto=True)
    fig.update_layout(title=dict(text=f'{prefecture} ',
                                font=dict(size=26,
                                        color='grey'),
                                y=0.98
                                ),
                    legend=dict(xanchor='center',
                                yanchor='bottom',
                                x=0.02,
                                y=0.83,
                                ),
                    width=700,
                    height=1500,
                    yaxis={'categoryorder':'total ascending'})
    #fig.show()
    st.plotly_chart(fig, use_container_width=True)

    st.title('日別平均G数順グラフ')
    # Here we use a column with categorical data
    fig = px.histogram(tenpobetsu_groupby_df,x="平均G数", y="店舗名", text_auto=True)
    fig.update_layout(title=dict(text=f'{prefecture} ',
                                font=dict(size=26,
                                        color='grey'),
                                y=0.98
                                ),
                    legend=dict(xanchor='center',
                                yanchor='bottom',
                                x=0.02,
                                y=0.83,
                                ),
                    width=700,
                    height=1500,
                    yaxis={'categoryorder':'total ascending'})
    #fig.show()
    st.plotly_chart(fig, use_container_width=True)
    extract_df['機種名'] = extract_df['機種名'].map(encoding_text)
    extract_df['店舗名'] = extract_df['店舗名'].astype(str)
    hibetu_df = extract_df.groupby(['日付','店舗名']).sum()
    hibetu_df['台数'] = extract_df.groupby(['日付','店舗名']).size()
    hibetu_df['1台平均差枚'] = hibetu_df['差枚'] / hibetu_df['台数']
    hibetu_df['平均出率'] =   (( hibetu_df['G数'] * 3) +  hibetu_df['差枚']) / (( hibetu_df['G数'] * 3)) *100 
    hibetu_df['平均G数'] =   hibetu_df['G数'] / hibetu_df['台数'] 
    hibetu_df['平均出率'] = hibetu_df['平均出率'].map(lambda x : round(x,1))
    hibetu_df['1台平均差枚'] = hibetu_df['1台平均差枚'].map(lambda x : round(x,1))
    hibetu_df = hibetu_df.reset_index()
    #hibetu_df['平均G数'] = hibetu_df['平均G数'].astype(int)
    #st.dataframe(hibetu_df)
    # hibetu_df['1台平均差枚'] = hibetu_df['1台平均差枚'].astype(int)
    # hibetu_df['G数'] = hibetu_df['G数'].astype(int)
    #hibetu_df['平均差枚'] = hibetu_df['平均差枚'].astype(float)
    hibetu_df = hibetu_df[['店舗名','日付','G数','差枚','台数','平均G数','1台平均差枚','平均出率']]
    st.title(f'日別店舗別データ(合計{len(hibetu_df)}店舗)')
    st.write(hibetu_df)
    csv = hibetu_df.to_csv(index=False) 
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{tenpo_name}_{select_date}_.csv">download</a>'
    st.markdown(f"日別店舗別データをダウンロードする {href}", unsafe_allow_html=True)
    #hibetu_df['平均出率'] = hibetu_df['平均出率'].astype(str)
    #hibetu_df['1台平均差枚'] = hibetu_df['1台平均差枚'].astype(str)


    #extract_df = extract_df.drop(['台番号'],axis=1)
    
    
    # st.title('日別総差枚グラフ')
    # samai_extract_df =   hibetu_df.drop(['G数','BB','RB','1台平均差枚','平均出率','台番号','台数','平均G数'],axis=1)
    # st.bar_chart(samai_extract_df)
    
    # st.title('日別平均G数グラフ')
    # samai_extract_df =   hibetu_df.drop(['G数','BB','RB','1台平均差枚','平均出率','台番号','台数','差枚'],axis=1)
    # st.bar_chart(samai_extract_df)
    
    
    # output_graph_whole_anaytics(extract_df)
    # goukei_samai = extract_df['差枚'].sum()
    # goukei_gamesuu = extract_df['G数'].sum()
    # nisuu = len(extract_df.groupby('日付').sum())
    # heikin_gamesuu = goukei_gamesuu / len(extract_df)
    # st.subheader(f'{nisuu}日分 平均G数 {int(heikin_gamesuu)}G ※ART中のG数を数えてない機種があるため正確な数字ではありません ')
    # st.subheader(f'{nisuu}日分 合計差枚 {goukei_samai}')
    # st.subheader(f'{nisuu}日分 平均差枚 {round(goukei_samai/len(extract_df),1)}')
    # st.subheader(f'{nisuu}日分 合計台数 {str(len(extract_df))}')
    # extract_df['差枚'] = extract_df['差枚'].astype(int)
    #st.write(extract_df)
    st.title(f'全台データ(合計{len(extract_df)}台分)')#
    
    st.write(extract_df)
    csv = extract_df.to_csv(index=False) 
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{tenpo_name}_{select_date}.csv">download</a>'
    st.markdown(f"全台データをダウンロードする {href}", unsafe_allow_html=True)


    kisyubetsu_df = extract_df.groupby(['日付','店舗名','機種名']).sum()
    kisyubetsu_df['台数'] = extract_df.groupby(['日付','店舗名','機種名']).size()
    kisyubetsu_df = kisyubetsu_df[kisyubetsu_df['台数'] > 1]

    kisyubetsu_df['平均差枚'] = kisyubetsu_df['差枚'] / kisyubetsu_df['台数']
    kisyubetsu_df['平均G数'] = kisyubetsu_df['G数'] / kisyubetsu_df['台数']
    kisyubetsu_df['平均差枚'] = kisyubetsu_df['平均差枚'].astype(int)
    kisyubetsu_df['差枚'] = kisyubetsu_df['差枚'].astype(int)
    kisyubetsu_df['平均G数'] = kisyubetsu_df['平均G数'].astype(int)
    kisyubetsu_df = kisyubetsu_df.reset_index()
    kisyubetsu_df = kisyubetsu_df.sort_values('差枚',ascending=False)
    #kisyubetsu_df = df.drop(['台番号','末尾','BB','RB'],axis=1)
    


    st.title('日別機種別抽出データ(バラエティを除く)')
    st.dataframe(kisyubetsu_df, width=2500, height=500)
    csv = kisyubetsu_df.to_csv(index=False)  
    b64 = base64.b64encode(csv.encode('utf-8-sig')).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{tenpo_name}_{select_date}.csv">download</a>'
    st.markdown(f"日別機種別データをダウンロードする {href}", unsafe_allow_html=True)
    
    
    #print(kisyubetsu_df)
    # if st.checkbox('バラエティは除く?(除く場合はチェック入れてもう一回検索ボタンおしえてね'):
    #     extract_df = query_database(tenpo_name,kisyu_name,select_date,last_day)
    #     kisyubetsu_df = extract_df.groupby(['日付','機種名']).sum()
    #     kisyubetsu_df['台数'] = extract_df.groupby(['日付','機種名']).size()
    #     print(kisyubetsu_df.columns)
    #     kisyubetsu_df = kisyubetsu_df.reset_index()
    #     kisyubetsu_df = kisyubetsu_df[kisyubetsu_df['台数'] > 1]
        
    
    samai_plus_kisyubetsu_df = kisyubetsu_df[kisyubetsu_df['差枚'] > 1]
    st.title('機種別バブルチャート(バラエティを除く、※右側の機種名をダブルクリックでその機種のみ表示になります)')
    fig = px.scatter(samai_plus_kisyubetsu_df, x='平均G数', y='平均差枚',
        size='差枚', color='機種名',
            hover_name='店舗名', log_x=True, size_max=60)
    st.plotly_chart(fig, use_container_width=True)
