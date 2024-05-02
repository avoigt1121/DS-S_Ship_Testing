# %%
import pandas as pd
import requests
import io
import sqlalchemy
from sqlalchemy import create_engine
import psycopg2

# %%
response = requests.get("https://api.open-notify.org/this-api-doesnt-exist") 
print(response.status_code)

# %%
response = requests.get("http://api.open-notify.org/astros") 
print(response.status_code)

# %%
print(response.json())

# %%
import json 

def jprint(obj): # create a formatted string of the Python JSON object 
    text = json.dumps(obj, sort_keys=True, indent=4) 
    print(text) 
    jprint(response.json())

# %%
jprint({ "message": "success", "number": 9, "people": [ { "craft": "ISS", "name": "Gennady Padalka" }, { "craft": "ISS", "name": "Mikhail Kornienko" }, { "craft": "ISS", "name": "Scott Kelly" }, { "craft": "ISS", "name": "Oleg Kononenko" }, { "craft": "ISS", "name": "Kimiya Yui" }, { "craft": "ISS", "name": "Kjell Lindgren" }, { "craft": "ISS", "name": "Sergey Volkov" }, { "craft": "ISS", "name": "Andreas Mogensen" }, { "craft": "ISS", "name": "Aidyn Aimbetov" } ] })

# %%
response = requests.get("https://api-server.dataquest.io/economic_data/countries") 
data = response.json()

# %%
response = requests.get("https://api-server.dataquest.io/economic_data/countries?filter_by=region=Sub-Saharan%20Africa")

# %%
data = response.json()

# %%
jprint(data)

# %%
import test
import os

from test import mytestvar

# %%
import config
from config import API_KEY
api_key = config.API_KEY

# %%
!curl "https://data.nasdaq.com/api/v3/datatables/MER/F1.xml?&mapcode=-5370&compnumber=39102&reporttype=A&qopts.columns=reportdate,amount&api_key={}".format(api_key)



# %%
url = 'data.nasdaq.com/api/v3/datatables/MER/F1.xml'

mapcode = -5370
comp_num = 39102

report = 'A'
qopts_ = 'reportdate,amount'

# %%

itry = f"https://{url}&reporttype={report}&api_key={api_key}"

print(itry)

# %%
res = requests.get(itry)
res

# %%
res = requests.get("https://data.nasdaq.com/api/v3/datatables/WIKI/PRICES.csv?&api_key={api_key}")

# %%
if res.status_code == 200:
    csv_data = io.BytesIO(res.content)
    df = pd.read_csv(csv_data)

    print(df.head)

# %%
res.content

# %%
setup.py build_ext --pg-config /path/to/pg_config build ...

# %%
df.to_sql('data',con=conn, if_exists ='replace',index=False)

# %%
conn_string = 'postgresql://postgres:postgres@localhost:5432'
db = create_engine(conn_string)
conn = db.connect

# %%



