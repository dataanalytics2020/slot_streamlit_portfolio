# ポートフォリオ
## アプリケーションの名前	
スロットデータビシュアライズ

## アプリケーションの概要	
このアプリケーションはパチンコ屋さんのデータをどの日にどの店舗が出ていたかをグラフ表示でき、素人の人でもわかりやすく調べられます。次遊びの行く店舗を参考にするため、勝つための分析が誰でもできるサイトです。

![site_image](https://user-images.githubusercontent.com/117744645/207402527-a3bd09f7-8e39-4301-a2d3-217eb8e3ba42.png)

## アプリケーションのURL	
https://pachislo7.com

## 制作背景	
趣味だったスロットで勝つためにこういうスロットのデータ分析サイトがあったらいいなを具現化しました。
※現在はプログラミングのせい（おかげ？）でスロットのレバーを叩くのがループ処理に感じて苦痛なためスロットは辞めました。

## 使用技術	
- Python 3.9.13
    - 外部ライブラリ一覧
    - selenium
    - webdriver-manager
    - requests
    - pandas
    - mysql.connector
    - plotly
    - dotenv
- venv
- Streamlit 1.15.2
- MYSQL 8.0
- AWS
    - VPC
    - EC2
    - RDS
    - Route53
- WordPress Domain
- Nginx
- Tmux
## 機能要件
### 検索機能一覧	
#### 画面
- 各種検索機能(サイドカラム)
    - 店舗名検索(自由入力)
    - 機種名検索(自由入力)
    - 都道府県検索(マルチボックス)
    - 日付検索(カレンダー形式)
    - 特定日検索(リスト選択形式)※7の付く日のみなど
    - 曜日指定検索(リスト選択形式)
- 分析機能一覧（メインカラム)
    - 店舗別概要分析(テーブル表示)
    - 店舗別平均差枚分析(横棒グラフ表示)
    - 店舗別平均G数分析(横棒グラフ表示)
    - 日別店舗別概要分析(テーブル表示)
    - 台番別分析(テーブル表示)
    - 日別機種別分析(テーブル表示)
    - 機種別バブルチャート分析(バブルチャート)


## 非機能要件
- サーバー費用は無料で収まるように調整
 
## 苦労した部分
本当は時間があればDjangoで開発したかったですが学習コストが高いのでpythonでもフロントエンドが実装できるStreamlitを採用しました。  

またSQLとサーバー技術の学習のためHerokuやstreamlit cloudなど簡単なデプロイサービスは使用せず、AWS上のサービス(EC2/RDS)を採用しました。  

ドメイン取得まで行い、実際にユーザーに対し、サービスとしてリリースできるまで作り上げました。

## こだわった部分
データの色々な表現手法（折れ線グラフや箱ひげ図etc...
)がある中でどんな分析方法と表現方法がスロットユーザーにとってどの情報に価値があるか、そしてわかりやすいか考え、どの店のどの機種が出ていたかが一目で見やすいようにサイトのＵＩを工夫しました。

検索機能に関しても様々な切り口の検索方法で対応でき、複数条件でもデータが出るように裏のSQLの構文と検索機能を工夫しました。

## 今後追加したい機能	
*『じゃあ明日どの店舗に行けば勝てるの？データ分析なんかできないよ！！』*  
  という人のために機械学習かルールベースで明日のおすすめ店舗とおすすめ機種をレコメンドする機能を組み込みたいです。

## ER図	
今後は取材予定テーブルと機種データテーブルを追加予定です。
![ER_image](https://user-images.githubusercontent.com/117744645/207644300-a43c0f30-b427-4c8c-b822-9852556f147b.png)

## 構成図	
![diagram](https://user-images.githubusercontent.com/117744645/207901420-52a50888-4521-40f7-bbf1-46c9d3f628ec.png)

# 起動手順（備忘録）

## EC2へのssh接続
ssh slot_streamlit

## 仮想化環境作成と起動
### windows仮想化環境作成
python3 -m venv venv
### windows仮想化環境起動
venv\Scripts\activate

### ec2仮想化環境作成
sudo python3 -m venv venv
### ec2仮想化環境起動
cd slot_streamlit_portfolio
source venv/bin/activate

## ブラウザ起動
streamlit run portfolio.py

## ライブラリ一括インストール
pip install -r requirements.txt

## GIT
### プル
sudo git pull 


## tmux のインストール
sudo yum install -y tmux

### streamlit の公開に使うセッションを作成
tmux new -s StreamSession

### アプリ公開
streamlit run portfolio.py