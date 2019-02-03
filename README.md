# Hello Neighbors
View the favorite neighborhoods of Neighborhoods.com employees on a map

# Overview 
The goal of this demo is to provide a playground that does the following
1. Use data from https://www.neighborhoods.com/about/our-team
1. Extract a favorite location from the biography (i.e `Alex's favorite neighborhood is West Loop in Chicago.`)
1. Attempt to geocode this location to turn the text into a point on the earth.
1. Present the points on an interactive map.

# Live Demo
This demo is up and running at [https://map.berryman.space/](https://map.berryman.space/)

# Things that still need improving
 - Geocoding unstructured text is unreliable. Look at [https://map.berryman.space/debug](https://map.berryman.space/debug) 
 to see the input and output of the geocoding for pins that look to be in an odd location.
   - Mapbox provides page to see what filters can applied [https://www.mapbox.com/search-playground](https://www.mapbox.com/search-playground)
 - The layout of the map hides points when they are overlapping, this makes finding a specific name difficult.
   - In Chicago there are a stacked points (i.e. Logan Square, or Wicker Park)  where people have the same favorite neighborhood. Offsetting the points slightly, or selecting a different POI can help spread out the points.
 - The color scheme and icons are boring.
 
# Resources
 - [Flask](http://flask.pocoo.org/) web microframework
 - [Requests](http://docs.python-requests.org/en/master/) API client
 - [Mapbox](https://www.mapbox.com/) provides [geocoding](https://github.com/mapbox/mapbox-sdk-py/blob/master/docs/geocoding.md#geocoding) and the Javascript [map API](https://www.mapbox.com/mapbox-gl-js/api/)

# Getting started on OSX
To get all the tools you'll need run, edit, and debug this code we'll use Brew to manage packages.

Follow the instructions at https://brew.sh/ which should tell you to use the following command:

`/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`

Now that `brew` is installed lets get our other tools:

`brew install git python3`

Grab the code from this repository:

`git clone git@github.com:alexberryman/hello-neighbors.git`

Change into the directory with code:

`cd hello-neighbors`

Create a virtual python environment to store out libraries:

`python3 -m venv env`

Activate the virtual environment:

`source env/bin/activate`

Install the necessary libraries:

`pip install -r requirements.txt`

Create a `settings.py` from the example:

`cp settings.py.example settings.py`

Create a Mapbox account at [https://www.mapbox.com](https://www.mapbox.com), place the key into `settings.py`

`vim settings.py`

Launch the app:

`APP_CONFIG_FILE="settings.py" python main.py`

Visit the page to see the map:

[http://127.0.0.1:8080/](http://127.0.0.1:8080/)

