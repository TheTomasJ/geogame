# GeoGame - simple strategic geographical game
## Semestral project in course of Advanced Databases Technologies (PDT FIIT STU 2016)

### Installation
1. Create new directory for this project
2. Download newest osm file from http://www.freemap.sk/index.php?c=core.download&filename=/slovakia.osm/
3. Pull this repo
4. Create new Posgtres db
5. Modify db settings in settings.py 

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '<your db name>',
        'USER': '<your username>',
        'PASSWORD': '<your db password>',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```

6. Load osm file to your db
7. run raw SQL (`INITIAL_MIGRATION`) written in settings.py to init db 
8. Locate console to project
9. Create project's virtual enviroment
10. run `pip install -r requirements.txt`
11. run `python manage.py runserver`
12. locate to http://127.0.0.1:8000
13. enjoy!

### How to play
1. This game is designed for two players (reds vs. blues)
2. A player can do only one action in a single step
..1. Manipulate population - assign population living in a city / town or village within the selected area on the map to increase a player's score
..2. Invest - increases area of effect
3. Player who controlls most of the country is the winner

### Important scenarios
1. Show three towns (cities) closest to the selected point (only towns (cities) with population higher than 10.000) - educative scenario
2. Get portion from non-manipulated area 
3. Remove polygon from 2nd step from non-manipulated area
4. Get population of towns (cities, villages) which are inside the selected polygon from step 2
5. Delete non-manipulated area and copy a new polygon of the whole Slovakia as a new non-manipulated area on every refresh of the page (new game)
