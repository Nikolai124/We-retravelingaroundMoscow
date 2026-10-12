from django.shortcuts import render
from django.http import HttpResponse
from places.models import Place


def main(request):
    places = Place.objects.all()
    info_places = {
      "type": "FeatureCollection",
      "features": [
        {
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [place.longitude, place.latitude]
          },
          "properties": {
            "title": place.name,
            "placeId": place.id,
            "detailsUrl": "./static/moscow_legends.json"
          }
        } for place in places
      ]
    }
    return render(request, 'index.html', {"info_places":info_places})

