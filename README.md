# ポートフォリオ
## アプリケーションの名前	
スロットデータビシュアライズ

## アプリケーションの概要	
このアプリケーションはパチンコ屋さんのデータを素人の人でもどの台がどれくらい出ていてか。
どの日にどの店舗が出ていたかなどをわかりやすく調べて勝ちにつなげる分析が誰でもできるサイトです。

## アプリケーションのURL	
https://pachislo7.com

## 制作背景	
趣味だったスロットで勝つために自分でこういう分析サイトがあったらいいなを具現化しました。
## 使用技術	

このアプリケーションで使用した技術を箇条書きで記述
## 機能一覧	
このアプリケーションで実装した機能を箇条書きで記述
## こだわった部分
こだわった部分やアピールしたい部分を記述（画像や動画を載せる）
## 苦労した部分	

## 今後追加したい機能	

## ER図	
ER図の画像を貼り付けます。
ER図とは一言で言うとデータベースの設計図です。
データベースにどのようなテーブルがあるのか、テーブルにはどのようなカラムがあるのか、テーブル同士はどのようなリレーション関係になっているのか、を図で表したものになります。

## インフラ構成図	
インフラ構成図の画像を貼り付けます。
インフラ構成図とはその名の通り、インフラの構成図です。どのような構成でインフラを構築したのかを図で表したものになります。


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