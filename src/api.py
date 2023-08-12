from flask import Flask, request, jsonify
from datetime import datetime, timedelta
from analytics import Analytics
from persistence import EventPersistence
from collections import Counter

app = Flask(__name__)


"""
API to serve data from the database

API endpoints
/events/raw (raw data from the database)
/events/frequency (error corrected, grouped by plate frequency)


OData query parameters
- $select to view only specific columns, use $select=timestamp,img_filename,ocr_result
- $filter to view only specific rows when a condition is true
    e.g. 
    - datetime ranges
    - relative time ranges
    - specific values

>Examples:
- Events from the last 24 hours: $filter=relative_time(last_24_hours)
- Events from the last 7 days:   $filter=relative_time(last_7_days)
- Events from the last 30 days:  $filter=relative_time(last_30_days)
- Events from the last 90 days:  $filter=relative_time(last_90_days)
- Events in date rangee (inclusive): $filter=timestamp ge 2020-01-01T00:00:00Z and timestamp le 2020-01-02T00:00:00Z

$filter=timestamp gt 2020-01-01T00:00:00Z and timestamp lt 2020-01-02T00:00:00Z
$select = timestamp, image, ocr_result
$filter=relative_time(last_24_hours)

https://zd-sales.zoominsoftware.io/bundle/console_user_guide_10y_console_saas-enus/page/console/topics/console_api_odata_bestpractices.html

"""

@app.route('/events/raw', methods=['GET'])
def get_events_raw():
    
        if request.method == 'GET':
    
            try:
                # parse the query string parameters
                query_params = request.args.to_dict()
                if "$select" in query_params and len(query_params["$select"]) > 0:
                    select_query = _build_select_query(query_params["$select"])
                else: 
                    select_query = "*"
                if "$filter" in query_params and len(query_params["$filter"]) > 0:
                    filter_query = _build_filter_query(query_params["$filter"])
                else:
                    filter_query = ""

                eventsDB = EventPersistence()
                events = eventsDB.query_events(select_query, filter_query)
                eventsDB.close()
    
                response = jsonify(events)
                response.status_code = 200
                return response
            
            except Exception as e:
                response = jsonify({"error": f"Error getting events - {e}"})
                response.status_code = 500
                return response
    
    
        return jsonify(events)

@app.route('/events/frequency', methods=['GET'])
def get_events_summary():

    if request.method == 'GET':
        try:
            query_params = request.args.to_dict()
            select_query = "*"
            if "$filter" in query_params and len(query_params["$filter"]) > 0:
                filter_query = _build_filter_query(query_params["$filter"])
            else:
                filter_query = ""

            analytics = Analytics()
            eventsDB = EventPersistence()
            events = eventsDB.query_events(select_query, filter_query)
            eventsDB.close()
    
            plates = []
            for event in events:
                timestamp, img_filename, ocr_result = event
                best_plate = analytics.get_best_plate(ocr_result)
                if best_plate != None:
                    plates.append(best_plate)
            
            # count the frequency of the plates 
            plate_count = Counter(plates)

            response = jsonify(plate_count)
            response.status_code = 200
            return response
        
        except Exception as e:
            response = jsonify({"error": f"Error getting events - {e}"})
            response.status_code = 500
            return response
        
    return jsonify(events)


def _build_select_query(select_params):
    valid_columns = {"timestamp", "img_filename", "ocr_result"}

    if len(select_params) == 0:
        return "*"

    cols = select_params.split(",")
    if len(cols) > 0:
        select_query = ""
        for col in cols:
            if len(select_query) > 0 and col in valid_columns:
                select_query += ","
            select_query += col.strip()

    return select_query
    
def _build_filter_query(filter_params):

    # TODO: evaluate logical conditions

    if filter_params.startswith("relative_time"):
        # relative time filter
        relative_time = filter_params.split("(")[1].split(")")[0]
        if relative_time == "last_24_hours":
            num_days = 1
        elif relative_time == "last_7_days":
            num_days = 7
        elif relative_time == "last_30_days":
            num_days = 30
        else:
            num_days = 0                

        now = datetime.now()
        start_ts = now - timedelta(days=num_days) 
        start_ts = start_ts.timestamp()
        end_ts = now.timestamp()
    
    else:
        # parse date range    
        # example: $filter=timestamp gt 2020-01-01T00:00:00Z and timestamp lt 2020-01-02T00:00:00Z
        # example: $filter=timestamp eq 2020-01-01T00:00:00Z 
        # example: $filter=timestamp ge 2020-01-01T00:00:00Z 
        # example: $filter=timestamp le 2020-01-01T00:00:00Z 
        """
        and
        or
        eq
        gt
        ge
        lt
        le
        ne
        not
        contains
        startswith
        """
        start_ts = datetime.now().timestamp()
        end_ts = start_ts
    
    start_ts = round(start_ts * 1000)
    end_ts = round(end_ts * 1000)

    filter_query = f"timestamp >= {start_ts} AND timestamp <= {end_ts}"
    return filter_query




"""
Function to process the query string parameters and create query 
"""



if __name__ == "__main__":
    app.run()
