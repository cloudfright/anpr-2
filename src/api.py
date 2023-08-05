from flask import Flask, request, jsonify
from datetime import datetime, timedelta
from analytics import Analytics
from persistence import EventPersistence
from collections import Counter

app = Flask(__name__)

@app.route('/events', methods=['GET'])
def get_events():

    if request.method == 'GET':

        try:
            eventsDB = EventPersistence()
            analytics = Analytics()
            start_ts = datetime.now() - timedelta(days=7) 
            start_ts = start_ts.timestamp()
            end_ts = datetime.now().timestamp()

            plates = []
            events = eventsDB.get_events(start_ts, end_ts)
            for event in events:
                timestamp, img_filename, ocr_result = event
                best_plate = analytics.get_best_plate(ocr_result)
                if best_plate != None:
                    plates.append(best_plate)
            
                # event["best_plate"] = analytics.get_best_plate(event["ocr_result"])
                # print(event)

            plate_count = Counter(plates)
            # # sort plate readings by frequency, descending
            # sorted_plates = sorted(plate_count.items(), key=lambda x: x[1], reverse=True)
            eventsDB.close()

            response = jsonify(plate_count)
            response.status_code = 200
            return response
        
        except Exception as e:
            response = jsonify({"error": f"Error getting events - {e}"})
            response.status_code = 500
            return response

  
    return jsonify(events)

if __name__ == "__main__":
    app.run()
