# 起動手順

## URL
htttps://pachislo7.com

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