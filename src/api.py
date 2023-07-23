from flask import Flask, request, jsonify
from datetime import datetime
from analytics import Analytics

app = Flask(__name__)

@app.route('/events', methods=['GET'])
def get_events():

    if request.method == 'GET':
        analytics = Analytics()
        events = analytics.getEventsInLast24Hours()
        response = jsonify(events)
        response.status_code = 200
        return response

  
    return jsonify(events)

if __name__ == "__main__":
    app.run()
