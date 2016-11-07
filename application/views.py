from django.shortcuts import render
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

def index(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            DELETE FROM freeland;
            INSERT INTO 
                freeland (way) 
            VALUES 
                (ST_Multi((SELECT way FROM planet_osm_polygon where name = 'Slovensko')))
            """)
    return render(request, 'index.html', {})

@csrf_exempt
def from_click(request):
    lat = request.POST['lat']
    lng = request.POST['lng']
    with connection.cursor() as cursor:
        sql = """
            SELECT 
                name, CAST(coalesce(population, '0') AS integer) AS popu, place, ST_Distance(
                    way,
                    ST_Transform(ST_SetSRID(ST_MakePoint(%s, %s), 4326),900913)
                )
            FROM 
                planet_osm_point as a 
            WHERE 
                (place = 'town' or place='village' or place='city') and CAST(coalesce(population, '0') AS integer) > 10000 
            ORDER BY
                ST_Distance(
                    way,
                    ST_Transform(ST_SetSRID(ST_MakePoint(%s, %s), 4326),900913)
                )
            LIMIT 3
            """ % (lng, lat, lng, lat)
        cursor.execute(
            sql
        )
        row = cursor.fetchall()
    return JsonResponse({'result':row})

@csrf_exempt
def colonise(request):
    lat = request.POST['lat']
    lng = request.POST['lng']
    distance = request.POST['distance']
    distance = int(distance)*1.5

    with connection.cursor() as cursor:

        # get targetet population
        sql = """
            SELECT 
                SUM(CAST(coalesce(population, '0') AS integer))
            FROM 
                planet_osm_point AS a
            WHERE 
                ST_Within(
                    a.way,
                    (SELECT ST_Multi(ST_Intersection(way,ST_Buffer(ST_Transform(ST_SetSRID(ST_MakePoint(%s, %s), 4326),900913), %s))) FROM freeland)
                )
                AND
                (place = 'town' OR place='village' OR place='city') 
            """ % (lng, lat, distance)
        cursor.execute(sql)
        row = cursor.fetchone()
        try:
            manipulated = int(row[0])
        except:
            manipulated = 0

        # get target portion
        sql = "SELECT ST_AsGeoJson(ST_Transform(ST_Multi(ST_Intersection(way,ST_Buffer(ST_Transform(ST_SetSRID(ST_MakePoint(%s, %s), 4326),900913), %s))), 4326)) FROM freeland" % (lng, lat, distance)
        cursor.execute(sql)
        row = cursor.fetchall()

        # update freeland
        sql = """
            UPDATE freeland SET way = ST_Multi(ST_Transform(
                ST_Difference(
                    ST_Transform(way,4326),
                    ST_Transform(ST_Buffer(ST_Transform(ST_SetSRID(ST_MakePoint(%s, %s), 4326),900913), %s),4326)
                ),
                900913
            ))
        """ % (lng, lat, distance)
        cursor.execute(sql)
        print manipulated

    return JsonResponse({'result':row, 'manipulated': str(manipulated)})

    """
            WITH RECURSIVE roads AS (
                (
                    SELECT a.name,a.way FROM planet_osm_line as a WHERE 
                    ST_Distance(way,ST_Transform(ST_SetSRID(ST_MakePoint(%s, %s), 4326),900913)) < 60
                    AND a.highway <> ''
                )
                UNION ALL
                (
                    SELECT b.name,b.way FROM planet_osm_line as b
                    JOIN roads ON ST_TOUCHES(roads.way,b.way) AND b.highway <> ''
                )
            ) SELECT ST_AsGeoJson(ST_Transform(way, 4326)) FROM roads LIMIT 4
            """

", ST_AsGeoJson(ST_Transform(way, 4326))"