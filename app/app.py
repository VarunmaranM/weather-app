from flask import Flask, render_template, jsonify
import requests
import os
from datetime import datetime

app = Flask(__name__)

# Get API key from environment variable
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', 'default_key')
VERSION = os.getenv('APP_VERSION', 'v1.0')

def get_weather(city="London"):
    """Get weather data from API"""
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

@app.route('/')
def index():
    """Main page"""
    weather = get_weather()
    return render_template('index.html', weather=weather, version=VERSION)

@app.route('/api/weather/<city>')
def weather_api(city):
    """API endpoint for weather data"""
    weather = get_weather(city)
    return jsonify(weather)

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'version': VERSION,
        'timestamp': datetime.utcnow().isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)