from django.conf import settings


def google_analytics(request):
    analytics_code = None
    if hasattr(settings, 'GOOGLE_ANALYTICS_CODE'):
        analytics_code = settings.GOOGLE_ANALYTICS_CODE
    return {'GOOGLE_ANALYTICS_CODE': analytics_code}