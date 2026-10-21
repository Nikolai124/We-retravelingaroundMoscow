from adminsortable2.admin import SortableAdminBase, SortableTabularInline
from django import forms
from django.contrib import admin
from django.utils.html import format_html
from tinymce.widgets import TinyMCE

from places.models import Place, PlaceImage


class ImagePreviewMixin:
    @admin.display(description="Превью")
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 100px;" />',
                obj.image.url,
            )


class PlaceImageInline(ImagePreviewMixin, SortableTabularInline):
    model = PlaceImage
    extra = 0
    can_delete = False
    readonly_fields = ("image_preview",)
    fields = ("image", "image_preview")


class PlaceAdminForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = "__all__"
        widgets = {"long_description": TinyMCE()}


@admin.register(Place)
class PlacesAdmin(SortableAdminBase, admin.ModelAdmin):
    form = PlaceAdminForm
    list_display = ["name"]
    inlines = [PlaceImageInline]


@admin.register(PlaceImage)
class PlaceImageAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display = ["place", "image", "image_preview"]
    list_select_related = ["place"]
