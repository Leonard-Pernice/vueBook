from django.apps import AppConfig


class BookdbConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bookDB"

    def ready(self):
        import bookDB.signals
