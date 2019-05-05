"""abarocks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import include, url
from django.urls import path, re_path, include
from django.contrib import admin

from django.views.generic import RedirectView

# wagtail CMS
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.core import urls as wagtail_urls

from .views import redirect_error_report, redirect_root, redirect_study, redirect_research, redirect_coffee, redirect_coffee_confirm, redirect_thanks

urlpatterns = [
    url(r'^error/report', redirect_error_report),
    url(r'^admin/', admin.site.urls),
    url(r'^research/', redirect_research),
    url(r'^coffee/', redirect_coffee),
    url(r'^thanks/', redirect_thanks),
    url(r'^blog_coffee_checkout/', redirect_coffee_confirm),
    url(r'^study/', redirect_study),
    url(r'^$', redirect_root),
    url(r'^blog/', include('blog.urls')),
    url(r'^pages/', include('pages.urls')),
    url(r'^quiz/', include('quiz.urls')),
    url(r'^polls/', include('polls.urls')),
    url(r'^fluency/', include('fluency.urls')),
    url(r'^learn/', include('learn.urls')),

    #wagtail CMS
    re_path(r'^cms/', include(wagtailadmin_urls)),
    re_path(r'^documents/', include(wagtaildocs_urls)),
    re_path(r'^wag_pages/', include(wagtail_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_title  = 'ABA.rocks Administration'
admin.site.site_header = 'ABA.rocks administration'
