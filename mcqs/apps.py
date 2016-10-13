from django.apps import AppConfig


class McqsConfig(AppConfig):
    name = 'mcqs'

    def ready(self):
        import mcqs.signals
