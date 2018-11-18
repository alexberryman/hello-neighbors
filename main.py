# [START gae_python37_app]
import json

import redis
import requests
import re
from flask import Flask, render_template
from geojson import FeatureCollection
from mapbox import Geocoder
from werkzeug.contrib.cache import SimpleCache

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('APP_CONFIG_FILE', silent=True)
MAPBOX_ACCESS_KEY = app.config['MAPBOX_ACCESS_KEY']

REDIS_HOST = app.config['REDIS_HOST']
REDIS_PORT = app.config['REDIS_PORT']
REDIS_PASSWORD = app.config['REDIS_PASSWORD']

if REDIS_HOST:
    cache = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)
else:
    cache = SimpleCache()


@app.route('/')
def get_index():
    return render_template('index.html', ACCESS_KEY=MAPBOX_ACCESS_KEY, )


@app.route('/debug')
def get_clickable():
    return render_template('debug.html', ACCESS_KEY=MAPBOX_ACCESS_KEY)


@app.route('/feature_collection')
def get_feature_collection():
    feature_collection = cache.get('feature_collection')
    if feature_collection is None:
        employees_data = create_employee_data()
        features = []
        for data in employees_data:
            if data['location_feature']:
                features.append(data['location_feature'])

        feature_collection = json.dumps(FeatureCollection(features))
        cache.set('feature_collection', feature_collection)

    return feature_collection


def create_employee_data():
    team_data = requests.get('https://www.neighborhoods.com/api/cms/ourteam')
    employees = extract_employee_fav_location(team_data)
    employees = geocode_favorite_spot(employees)

    return employees


def extract_employee_fav_location(team_data):
    employees = combine_employee_blocks(team_data)
    for offset, employee in enumerate(employees):
        pattern_for_location_text = re.compile(r'favorite neighborhood is(?P<location_text>.+)(?=\.|\<)', re.IGNORECASE)
        matched = pattern_for_location_text.search(employee['bio'])
        if matched:
            employees[offset]['location_text'] = matched.group('location_text')
        else:
            print('location not found for ' + employee['name'])
            employees[offset]['location_text'] = None
    return employees


def combine_employee_blocks(team_data):
    json_data = team_data.json()
    content_we_care_about = json_data['results'][0]['blocks']
    employees = []
    for key in content_we_care_about:
        if content_we_care_about[key]['type'] == 'employee-list':
            for employee in content_we_care_about[key]['employees']:
                employees.append(employee)
    return employees


def geocode_favorite_spot(employees):
    for index, employee in enumerate(employees):
        if employee['location_text']:
            forward_response = request_geocoding(employee)
            if forward_response.status_code == 200:
                if len(forward_response.geojson()['features']) > 0:
                    employees[index]['location_feature'] = forward_response.geojson()['features'][0]
                    employees[index]['location_point'] = forward_response.geojson()['features'][0]['geometry']
                    employees[index]['location_feature']['properties']["icon"] = 'marker'
                    employees[index]['location_feature']['properties']["name"] = employee['name']
                    employees[index]['location_feature']['properties']["bio"] = employee['bio']
                    employees[index]['location_feature']['properties']["location_text"] = employee['location_text']
                    employees[index]['location_feature']['properties']["place_name"] = \
                        forward_response.geojson()['features'][0]['place_name']
                    employees[index]['location_feature']['properties']["place_type"] = \
                        forward_response.geojson()['features'][0]['place_type'][0]
                else:
                    employees[index]['location_feature'] = None
                    employees[index]['location_point'] = None
                    print('geocode failed for ' + employee['name'] + ' using ' + employee['location_text'])
            else:
                print('geocode responded non-200 for ' + employee['name'] + ' using ' + employee['location_text'])
                employees[index]['location_feature'] = None
                employees[index]['location_point'] = None
        else:
            employees[index]['location_feature'] = None
            employees[index]['location_point'] = None

    return employees


def request_geocoding(employee):
    geocoder = Geocoder()
    geocoder.session.params['access_token'] = app.config['MAPBOX_ACCESS_KEY']
    forward_response = geocoder.forward(employee['location_text'])
    return forward_response


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
