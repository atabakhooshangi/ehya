from django.urls import path
from .views import GetInformsAPIView

app_name = 'Informs'

urlpatterns = [
    path('informs/<str:inform_type>', GetInformsAPIView.as_view(), name='Informs')
]
