import os
import re
import requests
import time
import pandas as pd
import pygsheets
import unicodedata
from bs4 import BeautifulSoup as bs
from datetime import datetime
from pytz import timezone

def extract_fk_price(url):
    request = requests.get(url)
    soup = bs(request.content,'html.parser')
    product_name = soup.find("span",{"class":"B_NuCI"}).get_text()
    new_str = unicodedata.normalize("NFKD", product_name)
    price = soup.find("div",{"class":"_30jeq3 _16Jk6d"}).get_text()
    prince_int = int(''.join(re.findall(r'\d+', price)))
    time_now = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M')
    return [new_str, prince_int, time_now]

path = 'PASTE_PATH_TO_GOOGLE_SHEET_API_JSON_FILE'
sheet_id = 'PASTE_GOOGLE_SHEET_ID_HERE'
URL = "PASTE_FK_PRODUCT_URL"
gc = pygsheets.authorize(service_account_file = path)
gsheet_1 = gc.open_by_key(sheet_id)

output = extract_fk_price(URL)
df = pd.DataFrame([output], columns = ["Product", "Price", "Date Time"])

ws_1 = gsheet_1.worksheet()
sheet_df = ws_1.get_as_df()

if sheet_df.empty:
    ws_1.set_dataframe(df,
                     (1,1))
else:
    df = pd.concat([sheet_df, df], 
                   ignore_index=True)
    ws_1.set_dataframe(df,
                     (1,1))

