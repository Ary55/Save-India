from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import ssl
import math

app = Flask(__name__)
app.secret_key = '6yTWFOE7j05WpVr8ic'

# database
client = MongoClient('mongodb://Shapin:Shapin@cluster0-shard-00-00-lnqyp.mongodb.net:27017,cluster0-shard-00-01-lnqyp.mongodb.net:27017,cluster0-shard-00-02-lnqyp.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority', ssl_cert_reqs=ssl.CERT_NONE)

db = client['Save-India']
hospitals = db['hospitals']

# finding hospitals in range


def get_hospitals_in_range(lat, lon, distance_range):
    earth_radius = 3958.75
    lat2 = lat
    lon2 = lon
    list_return = []

    list_of_hospitals = hospitals.find({})

    for docs in list_of_hospitals:
        lat1 = docs['lat']
        lon1 = docs['long']

        dlat = math.radians(lat2-lat1)
        dlon = math.radians(lon2 - lon1)

        sinDlat = math.sin(dlat / 2)
        sinDlon = math.sin(dlon / 2)

        a = math.pow(sinDlat, 2) + math.pow(sinDlon, 2) * \
            math.cos(math.radians(lat1)) * math.cos(math.radians(lat2))

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

        dist = earth_radius * c

        if (dist < distance_range):
            docs['dist'] = dist
            docs['_id'] = str(docs['_id'])
            list_return.append(docs)

    print(str(list_return))

    return list_return


@app.route('/')
def home_page():
    return render_template('index.html')

# get markers
@app.route('/get_markers', methods=['GET'])
def get_markers():
    lat = float(request.args['lat'])
    lon = float(request.args['lon'])
    dist_range = float(request.args['dist_range'])

    h = get_hospitals_in_range(lat, lon, dist_range)

    return jsonify(h)


if __name__ == '__main__':
    app.run(debug=True)
