from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/news/analyze', methods=['POST'])
def analyze_news():
    data = request.get_json()
    # Process the data...
    return jsonify({"message": "Data received successfully"})

    # Dummy response (replace with real logic)
    return jsonify({
        "sentiment": "positive",
        "confidence": 0.95,
        "symbol": symbol,
        "text": text
    })

if __name__ == '__main__':
    app.run(port=5001)
