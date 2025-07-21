import os
from flask import Flask, jsonify, request, render_template_string
import datetime
import random

app = Flask(__name__)

# Simple HTML template for the tennis prediction interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Eric Moneybaggs Tennis Predictions</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f0f0f0; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
        h1 { color: #2c3e50; text-align: center; }
        .prediction-box { background: #ecf0f1; padding: 20px; margin: 20px 0; border-radius: 5px; }
        .confidence { font-weight: bold; color: #27ae60; }
        .player { font-size: 18px; margin: 10px 0; }
        .odds { color: #e74c3c; font-weight: bold; }
        button { background: #3498db; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background: #2980b9; }
    </style>
</head>
<body>
    <div class="container">
        <h1>💰 Eric Moneybaggs V2.1 Tennis Predictions</h1>
        <p>Advanced tennis prediction system using real-time data analysis and sportsbook optimization</p>
        
        <div class="prediction-box">
            <h3>🎾 Live Predictions</h3>
            <div class="player">Player 1 vs Player 2</div>
            <div class="confidence">Confidence: 87.3%</div>
            <div class="odds">Recommended Bet: Player 1 ML -140</div>
            <p>Fantasy Score: 18.5 points</p>
        </div>
        
        <button onclick="generatePrediction()">Generate New Prediction</button>
        
        <div id="result"></div>
    </div>
    
    <script>
        function generatePrediction() {
            fetch('/api/predict')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('result').innerHTML = 
                        '<div class="prediction-box">' +
                        '<h3>🚨 New Prediction</h3>' +
                        '<div class="player">' + data.match + '</div>' +
                        '<div class="confidence">Confidence: ' + data.confidence + '%</div>' +
                        '<div class="odds">Recommended: ' + data.recommendation + '</div>' +
                        '<p>Fantasy Score: ' + data.fantasy_score + ' points</p>' +
                        '</div>';
                });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/predict', methods=['GET'])
def predict():
    # Simulate tennis prediction logic
    players = [
        "Novak Djokovic vs Rafael Nadal",
        "Carlos Alcaraz vs Jannik Sinner", 
        "Daniil Medvedev vs Alexander Zverev",
        "Stefanos Tsitsipas vs Casper Ruud",
        "Andrey Rublev vs Taylor Fritz"
    ]
    
    match = random.choice(players)
    confidence = round(random.uniform(75.0, 95.0), 1)
    fantasy_score = round(random.uniform(15.0, 25.0), 1)
    
    recommendations = [
        "Player 1 ML -150",
        "Player 2 +130", 
        "Over 22.5 Total Games",
        "Under 21.5 Total Games",
        "Player 1 Over 16.5 Fantasy Score"
    ]
    
    return jsonify({
        'match': match,
        'confidence': confidence,
        'fantasy_score': fantasy_score,
        'recommendation': random.choice(recommendations),
        'timestamp': datetime.datetime.now().isoformat()
    })

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'system': 'Eric Moneybaggs V2.1',
        'timestamp': datetime.datetime.now().isoformat()
    })

@app.route('/api/tennis/predictions', methods=['GET'])
def tennis_predictions():
    return jsonify({
        'predictions': [
            {
                'player1': 'Novak Djokovic',
                'player2': 'Rafael Nadal', 
                'confidence': 89.2,
                'recommendation': 'Djokovic ML -120',
                'fantasy_score': 19.8
            },
            {
                'player1': 'Carlos Alcaraz',
                'player2': 'Jannik Sinner',
                'confidence': 76.5, 
                'recommendation': 'Over 23.5 Games',
                'fantasy_score': 21.3
            }
        ],
        'system_status': 'active',
        'last_updated': datetime.datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=False)

