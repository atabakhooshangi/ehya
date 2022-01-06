from django.urls import path
from .views import post_list_api, retrieve_post_api

# PostGetAPIView, RetrievePostAPIView, CreateCommentAPIView,
app_name = 'Homes'

urlpatterns = [
    # path('get_posts', PostGetAPIView.as_view(), name='Posts'),
    # path('get_post', RetrievePostAPIView.as_view(), name='Get-Post'),
    # path('create_comment', CreateCommentAPIView.as_view(), name='Create-Comment'),
    path('posts_list', post_list_api, name='Post-List'),
    path('retrieve_post', retrieve_post_api, name='Retrieve-Post'),

]
