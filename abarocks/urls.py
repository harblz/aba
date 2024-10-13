from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin

from debug_toolbar.toolbar import debug_toolbar_urls

import abarocks.settings
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("about", views.about, name="about"),
    path("patreon", views.patreon, name="patreon"),
    path("login/", views.login, name="login"),
    path("blog/", include("blog.urls")),
    path("quizzes/", include("quiz.urls")),
    path("learn/", include("learn.urls")),
    path("ckeditor5/", include("django_ckeditor_5.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.ENABLE_DEBUG_TOOLBAR:
    urlpatterns = [
        *urlpatterns,
    ] + debug_toolbar_urls()

admin.site.site_title = "ABA.rocks Administration"
admin.site.site_header = "ABA.rocks administration"
