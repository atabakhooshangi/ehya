from django.urls import path
from .views import CategoryListAPIView, CategoryTreeRetrieveAPIView, \
    CategoryRetrieveAPIView, PostsListView, PostRetrieveAPIView, CreateCommentAPIView, DeleteCommentAPIView, \
    PostsSearchView, TagListAPIView, AddOrRemovePostToLikesAPIView, GetUserSearchHistory

app_name = 'Homes'

urlpatterns = [
    path('category_list', CategoryListAPIView.as_view(), name='Categories'),
    path('category_tree/<int:pk>', CategoryTreeRetrieveAPIView.as_view(), name='Category Tree'),
    path('category/<int:pk>', CategoryRetrieveAPIView.as_view(), name='Category'),
    path('posts_list/<id>', PostsListView.as_view(), name='Post-List'),
    path('get_search_history', GetUserSearchHistory.as_view(), name='Get-Search-History'),
    path('like/<int:post_id>', AddOrRemovePostToLikesAPIView.as_view(), name='Post-Like'),
    path('posts_search', PostsSearchView.as_view(), name='Post-Search'),
    path('single_post/<int:pk>', PostRetrieveAPIView.as_view(), name='Post-Singe'),
    path('create_comment', CreateCommentAPIView.as_view(), name='Create-Comment'),
    path('delete_comment/<int:pk>', DeleteCommentAPIView.as_view(), name='Delete-Comment'),
    path('tags_list', TagListAPIView.as_view(), name='Tag-List'),

]
