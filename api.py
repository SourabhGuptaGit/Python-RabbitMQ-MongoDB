from flask import Flask, request, jsonify
import pymongo
import datetime

app = Flask(__name__)

MONGO_URI = "mongodb://localhost:27017"
MONGO_DB = "iot_data"
MONGO_COLLECTION = "status_collection"

client = pymongo.MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

@app.route('/status_count', methods=['GET'])
def get_status_count():
    start_time = request.args.get('start')
    end_time = request.args.get('end')
    print(f"start_time  -->  {start_time}")
    print(f"end_time  -->  {end_time}")
    try:
        # start_time = True
        # end_time = True
        # pass
        start_time = datetime.datetime.fromisoformat(start_time)
        end_time = datetime.datetime.fromisoformat(end_time)
    except ValueError:
        return jsonify({"error": "Invalid date format. Use ISO format."}), 400

    pipeline = [
        {"$match": {"timestamp": {"$gte": start_time, "$lte": end_time}}},
        {"$group": {"_id": "$status", "count": {"$sum": 1}}}
    ]

    result = collection.aggregate(pipeline)
    response = {str(item["_id"]): item["count"] for item in result}

    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
