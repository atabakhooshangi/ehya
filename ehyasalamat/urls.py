from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="احیا سلامت",
        default_version='v1',
        description="Exchange Compony Fobodex",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="tarbasi@outlook.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/auth/', include('accounts.urls', namespace='Accounts')),
    path('api/ticket/', include('ticket.urls', namespace='Tickets')),
    path('api/informs/', include('informs.urls', namespace='Informs')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
