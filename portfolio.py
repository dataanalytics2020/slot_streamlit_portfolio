import streamlit as st
import mysql.connector
import pandas as pd
import base64
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(layout="wide")
st.title("ポートフォリオ")