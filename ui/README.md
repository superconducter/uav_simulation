# UI: API & Map

- Map based on [LeafletSim Plugin](ui/frontend/static/lib/LeafletSim/README.md)
- Use HTTP status codes
- Direct SimPy integration

## Install

Note: All commands should in general be run from the root folder of the project.

Using the [Django Rest Framework Tutorial](http://www.django-rest-framework.org/tutorial/quickstart/)

```
pip install -r requirements.txt
#Or install manually:
pip install django
pip install djangorestframework


# Optional tool
pip install httpie
```

## Run

```
#Needs to be run in the root project folder e.g. asp_ss2016_main
python ui/manage.py makemigrations
python ui/manage.py makemigrations ui_sim_interface
python ui/manage.py migrate
python ui/manage.py runserver

```

## Generate data

Run the DemoDataGenerator to get Data into the database in a new shell:

```
python ui/DemoDataGenerator.py

# Visit in the browser:
# http://127.0.0.1:8000/
```



### Superuser

Create credentials:
```
python ui/manage.py createsuperuser
```

### Leaflet Playback Map

- entry point: /app/components/map/mapController.js
    - data from API is set here
- map class: /map.js
    - init. leaflet playback
    - adds static elements
    - displays object details in sidebar
- map controller: /map.controller.js
    - contains GUI elements (play/stop/...) still in html - no angular template
- map demo data: /components/data/demoDataFactory.js
    - for debugging (used if no api data available)
- map events: /map.event.js
    - handles events
        - sidebar
        - display as icon on map (custom icons)
    - triggered by LeafletPlayback.TrackController.handleEvents
- defines icon style on map: LeafletPlayback.TrackController.getMarkerIcon


# Sample configuration
A sample configuration can be found in
```
ui/frontend/static/simcore_demosettings.json
```