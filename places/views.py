from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
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
            "detailsUrl": reverse("place_details", args=[place.id])
          }
        } for place in places
      ]
    }
    return render(request, 'index.html', {"info_places":info_places})


def parse_place_details(request, place_id):
    place = get_object_or_404(Place.objects.prefetch_related("images"), pk=place_id)
    images_urls = [place_image.image.url for place_image in place.images.all()]
    payload = {
        'title': place.name,
        'imgs': images_urls,
        'description_short': place.short_description,
        'description_long': place.long_description,
        'coordinates': {
            'lng': place.longitude,
            'lat': place.latitude,
        }
    }
    return JsonResponse(payload, json_dumps_params={'ensure_ascii': False})
