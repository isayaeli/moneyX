from django.conf import settings

def app_id(self):
    app_id = settings.APP_ID
    app_id = {
        'app_id':app_id
    }
    return app_id