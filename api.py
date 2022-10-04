from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def index():
    return "Web jadwal sholat"

@app.route("/jadwal", methods = ["GET", "POST"])
def jadwal():
    if request.method == "POST":

        # From json
        id = request.json['id']
        m = request.json['m']
        y = request.json['y']
        d = request.json["d"]

        #Scraping
        url = "https://jadwalsholat.org/jadwal-sholat/monthly.php?"
        headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}
        params = {"id":id, "m":m, "y":y}
        res = requests.get(url, headers=headers, params=params)
        soup = BeautifulSoup(res.text, "html.parser")
        a = soup.find(attrs={"class":"table_adzan"})  

        hasil = []
        for i in a:
            try:
                if i['class']==['table_highlight'] or i['class']==['table_light'] or i['class']==['table_dark']:
                    hasil.append(i)
            except:
                pass
        
        result = {}

        for j in hasil:
            tanggal = int(j.findAll("td")[0].get_text())
            Imsyak = j.findAll("td")[1].get_text()
            Shubuh = j.findAll("td")[2].get_text()
            Terbit = j.findAll("td")[3].get_text()
            Dhuha = j.findAll("td")[4].get_text()
            Dzuhur = j.findAll("td")[5].get_text()
            Ashar = j.findAll("td")[6].get_text()
            Maghrib = j.findAll("td")[7].get_text()
            Isya = j.findAll("td")[8].get_text()
            result[tanggal] = {"Imsyak":Imsyak, "Shubuh":Shubuh, "Terbit":Terbit, "Dhuha":Dhuha, "Dzuhur":Dzuhur, "Ashar":Ashar, "Maghrib":Maghrib, "Isya":Isya}

        return jsonify(result[d])

    return "Gunakan method POST"
    