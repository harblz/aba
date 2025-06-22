from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin
from django.views.generic import TemplateView
from . import views
from core import views as core

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("about/", views.about, name="about"),
        path("blog/", include("blog.urls")),
        path("quizzes/", include("quiz.urls")),
        path("learn/", include("learn.urls")),
        path("safmeds/", include("safmeds.urls")),
        path("ckeditor5/", include("django_ckeditor_5.urls")),
        path("", views.home, name="home"),
        path("accounts/signup/", core.SignUpView.as_view(), name="signup"),
        path("accounts/", include("django.contrib.auth.urls")),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)

if settings.ENABLE_DEBUG_TOOLBAR:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns = [
        *urlpatterns,
    ] + debug_toolbar_urls()

admin.site.site_title = "ABA.rocks Administration"
admin.site.site_header = "ABA.rocks administration"
