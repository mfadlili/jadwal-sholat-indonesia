import requests
from bs4 import BeautifulSoup
import streamlit as st
import datetime
import pandas as pd

# Scraping kota & id kota
url = "https://jadwalsholat.org/jadwal-sholat/monthly.php"
headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}
res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, "html.parser")
a = soup.find(attrs={"class":"table_adzan"})
daftar_kota = {}
for id in a.findAll("option"):
    daftar_kota[id.get_text()] = int(id['value'])

st.title("Waktu Sholat Indonesia")

#Widget input kota
kota = st.selectbox(
    'Pilih kota',
    daftar_kota.keys())
id = int(daftar_kota[kota])

#Widget input tanggal
date = st.date_input("Input tanggal", datetime.datetime.now())
date_list = str(date).split("-")

y = int(date_list[0])
m = int(date_list[1])
d = int(date_list[2])

# Tampilkan hasil
send = {"id":id, "d":d, "m":m, "y":y}

if st.button('Cari'):
    result = requests.post("http://127.0.0.1:5000/jadwal", json=send)
    st.write("Jadwal Sholat di "+kota)
    df = pd.DataFrame([result.json()])
    st.write(df)