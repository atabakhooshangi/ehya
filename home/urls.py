from django.urls import path
from .views import PostGetAPIView, RetrievePostAPIView, CreateCommentAPIView

app_name = 'Home'

urlpatterns = [
    path('get_posts', PostGetAPIView.as_view(), name='Posts'),
    path('get_post', RetrievePostAPIView.as_view(), name='Get-Post'),
    path('create_comment', CreateCommentAPIView.as_view(), name='Create-Comment'),

]
