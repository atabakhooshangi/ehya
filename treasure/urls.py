from django.urls import path
from .views import CreateTreasureAPIView, GetAllTreasuresAPIView, RetrieveTreasuresAPIView, GetTreasureAnswerAPIView

app_name = 'Treasure'

urlpatterns = [
    path('create_get_treasure', CreateTreasureAPIView.as_view(), name='Create-Treasure'),
    path('get_treasures', GetAllTreasuresAPIView.as_view(), name='Get-Treasures'),
    path('retrieve_treasure', RetrieveTreasuresAPIView.as_view(), name='Get-Treasure'),
    path('treasure_message', GetTreasureAnswerAPIView.as_view(), name='Treasure-Message'),

]
