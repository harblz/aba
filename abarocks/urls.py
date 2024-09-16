"""abarocks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  re_path(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  re_path(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  re_path(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static

#from django.conf.urls import include, url
from django.urls import path, re_path, include
from django.contrib import admin

from django.views.generic import RedirectView

# wagtail CMS
#from wagtail.admin import urls as wagtailadmin_urls
#from wagtail.documents import urls as wagtaildocs_urls
#from wagtail.core import urls as wagtail_urls

from .views import redirect_error_report, redirect_root, redirect_study, redirect_research, redirect_coffee, redirect_coffee_confirm, redirect_thanks

urlpatterns = [    
    re_path(r'^admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    re_path(r'^error/report', redirect_error_report),
    re_path(r'^research/', redirect_research),
    re_path(r'^coffee/', redirect_coffee),
    re_path(r'^thanks/', redirect_thanks),
    re_path(r'^blog_coffee_checkout/', redirect_coffee_confirm),
    re_path(r'^study/', redirect_study),
    re_path(r'^$', redirect_root),
    re_path(r'^blog/', include('blog.urls')),
    re_path(r'^pages/', include('pages.urls')),
    re_path(r'^quiz/', include('quiz.urls')),
    re_path(r'^polls/', include('polls.urls')),
    re_path(r'^fluency/', include('fluency.urls')),
    re_path(r'^learn/', include('learn.urls')),

    # django newsletter
    #re_path(r'^newsletter/', include('newsletter.urls')),
    #re_path(r'^tinymce/', include('tinymce.urls')),

    # wagtail CMS
    #re_path(r'^cms/', include(wagtailadmin_urls)),
    #re_path(r'^documents/', include(wagtaildocs_urls)),
    #re_path(r'^wag_pages/', include(wagtail_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_title  = 'ABA.rocks Administration'
admin.site.site_header = 'ABA.rocks administration'
