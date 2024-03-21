from django.contrib import admin
from django.apps import apps

app_name = "accountant_pro"

app_config = apps.get_app_config(app_name)

# Get all models from the specified app
app_models = app_config.get_models()

# Register all models from the specified app with the admin site
for model in app_models:
    admin.site.register(model)
