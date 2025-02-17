from django.apps import AppConfig


class PolicyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'policy'

    def ready(self):
        import policy.signals  # Ensures signals are connected