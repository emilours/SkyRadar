import os
from dotenv import load_dotenv
import requests
from flask import Flask, render_template, request

load_dotenv()  # Charge le fichier .env
api_key = os.getenv("API_KEY")

app = Flask(__name__)

def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=fr"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        description = data['weather'][0]['description']
        return temp, description
    else:
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        city = request.form["city"]
        result = get_weather(city)
        if result:
            temp, description = result  # Décompose le résultat
            return render_template("index.html", city=city, temp=temp, description=description)
        else:
            return render_template("index.html", error="Erreur : Ville non trouvée ou problème de connexion.")
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
