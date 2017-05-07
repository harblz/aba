from django.conf import settings
from django.template.loader import render_to_string

def analytics(request):
    if settings.DEBUG:
        return { 'analytics_code': render_to_string("analytics/analytics.html", { 'google_analytics_key: settings.GOOGLE_ANALYTICS_PROPERTY_ID }) }
    else:
        return { 'analytics_code': "" }
