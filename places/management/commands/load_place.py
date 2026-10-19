import json
from urllib.error import URLError
from urllib.parse import quote, urlsplit, urlunsplit
from urllib.request import urlopen

from django.core.management.base import BaseCommand, CommandError

from places.models import Place


def read_json(source):
    if source.startswith(("http://", "https://")):
        parts = urlsplit(source)
        url = urlunsplit(parts._replace(path=quote(parts.path, safe="/%")))
        try:
            with urlopen(url, timeout=10) as response:
                raw = response.read().decode("utf-8")
        except URLError as error:
            raise CommandError(f"Не удалось скачать {source}: {error}")
    else:
        try:
            with open(source, encoding="utf-8") as file:
                raw = file.read()
        except FileNotFoundError:
            raise CommandError(f"Файл не найден: {source}")

    try:
        return json.loads(raw)
    except json.JSONDecodeError as error:
        raise CommandError(f"Невалидный JSON в {source}: {error}")


class Command(BaseCommand):
    help = "Загружает место из JSON-файла или по URL"

    def add_arguments(self, parser):
        parser.add_argument("sources", nargs="+", help="путь или URL к JSON-файлу места")

    def handle(self, *args, **options):
        loaded = 0
        for source in options["sources"]:
            data = read_json(source)
            try:
                place, created = Place.objects.update_or_create(
                    name=data["title"],
                    defaults={
                        "short_description": data["description_short"],
                        "long_description": data["description_long"],
                        "latitude": data["coordinates"]["lat"],
                        "longitude": data["coordinates"]["lng"],
                    },
                )
            except (KeyError, TypeError) as error:
                raise CommandError(f"В {source} нет нужного поля: {error}")

            action = "Создано" if created else "Обновлено"
            self.stdout.write(f"{action}: {place.name}")
            loaded += 1

        self.stdout.write(self.style.SUCCESS(f"Загружено мест: {loaded}"))
