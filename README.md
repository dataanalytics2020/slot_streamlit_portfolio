"# slot_streamlit_portfolio" 
##起動手順
###ssh接続
ssh slot_streamlit




#仮想化環境作成と起動
##windows
python3 -m venv venv
venv\Scripts\activate

##ec2
sudo python3 -m venv venv
source venv/bin/activate


##ライブラリ一括インストール
pip install -r requirements.txt

