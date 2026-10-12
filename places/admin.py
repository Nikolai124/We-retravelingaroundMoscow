from django.contrib import admin
from places.models import Place, PlaceImage
# Register your models here.

@admin.register(Place)
class PlacesAdmin(admin.ModelAdmin):
    list_display = ["name",]


@admin.register(PlaceImage)
class PlaceImageAdmin(admin.ModelAdmin):
    list_display = ["place", "image",]