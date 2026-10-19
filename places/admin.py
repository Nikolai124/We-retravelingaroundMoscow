from django import forms
from django.contrib import admin
from places.models import Place, PlaceImage
from adminsortable2.admin import SortableTabularInline, SortableAdminBase
from django.utils.html import format_html
from tinymce.widgets import TinyMCE
# Register your models here.

class PlaceImageInline(SortableTabularInline):
    model = PlaceImage
    extra = 0
    can_delete = False
    readonly_fields = ("image_preview",)
    fields = ("image", "image_preview")
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 100px;" />',
                obj.image.url
            )
    image_preview.short_description = "Превью"


class PlaceAdminForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = "__all__"
        widgets = {"long_description": TinyMCE()}


@admin.register(Place)
class PlacesAdmin(SortableAdminBase, admin.ModelAdmin):
    form = PlaceAdminForm
    list_display = ["name",]
    inlines = [PlaceImageInline]



@admin.register(PlaceImage)
class PlaceImageAdmin(admin.ModelAdmin):
    list_display = ["place", "image", "image_preview"]
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 100px;" />',
                obj.image.url
            )
    image_preview.short_description = "Превью"
