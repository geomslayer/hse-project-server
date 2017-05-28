from django.apps import AppConfig


class ApiAppConfig(AppConfig):
    name = 'api_app'

    def ready(self):
        from .models import Category
        from .settings import CATS

        try:
            if Category.objects.all().count() == 0:
                for cat in CATS:
                    new_cat = Category(text=cat)
                    new_cat.save()
        except Exception:
            pass
