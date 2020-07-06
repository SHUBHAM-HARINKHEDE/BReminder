from django.apps import AppConfig


class UserConfig(AppConfig):
    name = 'user'
    #signal to create profile when user created
    def ready(self):
        import user.signals

