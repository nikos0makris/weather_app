from flask import Flask, request, jsonify, render_template
import requests
from config import API_KEY, BASE_URL

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({'error': 'City parameter is required'}), 400

    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if response.status_code != 200:
        return jsonify(data), response.status_code

    weather = {
        'city': data['name'],
        'temperature': data['main']['temp'],
        'description': data['weather'][0]['description'],
        'icon': data['weather'][0]['icon']
    }
    return jsonify(weather)


if __name__ == '__main__':
    app.run(debug=True)
