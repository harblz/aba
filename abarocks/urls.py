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
from django.urls import path, re_path, include
from django.contrib import admin

from debug_toolbar.toolbar import debug_toolbar_urls

import abarocks.settings
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    # path("blog/", include("blog.urls")),
    path("quizzes/", include("quiz.urls")),
    # path("fluency/", include("fluency.urls")),
    path("learn/", include("learn.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.ENABLE_DEBUG_TOOLBAR:
    urlpatterns = [
        *urlpatterns,
    ] + debug_toolbar_urls()

admin.site.site_title = "ABA.rocks Administration"
admin.site.site_header = "ABA.rocks administration"
