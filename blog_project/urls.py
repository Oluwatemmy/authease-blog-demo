from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from blog import frontend_views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Blog API",
        default_version='v1',
        description="A simple blog API with authease authentication",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/auth/', include('authease.auth_core.urls')),
    path('api/oauth/', include('authease.oauth.urls')),
    path('api/blog/', include('blog.urls')),

    # Swagger docs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # Auth frontend (from authease package)
    path('accounts/', include('authease.auth_core.frontend_urls')),

    # OAuth frontend
    path('oauth/github/login/', frontend_views.github_login, name='github-login'),
    path('oauth/github/callback/', frontend_views.github_callback, name='github-callback'),
    path('oauth/google/login/', frontend_views.google_login, name='google-login'),
    path('oauth/google/callback/', frontend_views.google_callback, name='google-callback'),

    # Blog frontend
    path('', include('blog.frontend_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
