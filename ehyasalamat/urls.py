from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.generators import OpenAPISchemaGenerator

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from fcm_django.api.rest_framework import FCMDeviceViewSet, FCMDeviceAuthorizedViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'devices', FCMDeviceViewSet)


# schema_view = get_schema_view(
#     openapi.Info(
#         title="احیا سلامت",
#         default_version='v1',
#         description="Exchange Compony Fobodex",
#         terms_of_service="https://www.google.com/policies/terms/",
#         contact=openapi.Contact(email="tarbasi@outlook.com"),
#         license=openapi.License(name="BSD License"),
#     ),
#     public=True,
#     permission_classes=(permissions.AllowAny,),
# )


class CustomerGeneratorSchema(OpenAPISchemaGenerator):
    def get_operation(self, *args, **kwargs):
        operation = super().get_operation(*args, **kwargs)
        your_header = openapi.Parameter(
            name="Authorization",
            description="Description",
            required=False,
            in_=openapi.IN_HEADER,
            type=openapi.TYPE_STRING,
            default='Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ2MzEyNDcwLCJqdGkiOiI3MzkxY2Y3YmQzZmI0ZDc2YTg5M2NkMjllOWM0ZmU1MiIsInVzZXJfaWQiOiJkZjAwZTEzYi1mNTk1LTRhOTgtOTViNS01ZGFkNDBmYzY5MjkifQ.Sgco5LWCwD9Nu4NDNi1R7Hzzw_Q4Rrj87CJGRoJUXes')
        id_header = openapi.Parameter(
            name="id",
            description="Description",
            required=False,
            in_=openapi.IN_HEADER,
            type=openapi.TYPE_STRING,
            default=None
        )
        operation.parameters.append(your_header)
        operation.parameters.append(id_header)
        return operation


schema_view = get_schema_view(
    openapi.Info(
        title="احیا سلامت",
        default_version='v1',
        description="Ehya Salamat Application",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="tarbasi@outlook.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    # generator_class=CustomerGeneratorSchema
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    # path('jet/', include('jet.urls', namespace='jet')),
    # path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/auth/', include('accounts.urls', namespace='Accounts')),
    path('api/fcm/', include(router.urls)),
    path('api/ticket/', include('ticket.urls', namespace='Tickets')),
    path('api/informs/', include('informs.urls', namespace='Informs')),
    path('api/treasure/', include('treasure.urls', namespace='Treasure')),
    path('api/support/', include('support.urls', namespace='Support')),
    path('api/home/', include('wphome.urls', namespace='Homes')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
