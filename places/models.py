from django.db import models

class Place(models.Model):
    name = models.CharField("название", max_length=200)
    short_description = models.TextField("краткое описание")
    long_description = models.TextField("полное описание")
    latitude = models.DecimalField("широта", max_digits=50, decimal_places=30)
    longitude = models.DecimalField("долгота", max_digits=50, decimal_places=30)

    def __str__(self):
        return self.name


class PlaceImage(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="images", verbose_name="место")
    image = models.ImageField("картинка", upload_to="places/")
    order = models.PositiveIntegerField("порядок", default=0, db_index=True)

    class Meta:
        ordering = ["order"]
    
