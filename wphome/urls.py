from django.urls import path
from .views import (CategoryListAPIView, CategoryTreeRetrieveAPIView,
                    CategoryRetrieveAPIView, PostsListView, PostRetrieveAPIView, CreateCommentAPIView,
                    DeleteCommentAPIView,
                    PostsSearchView, TagListAPIView, AddOrRemovePostToLikesAPIView, #GetUserSearchHistory,
                    AddOrRemovePostToFavoriteAPIView, AddPostToViewsAPIView , UserFavoritePostsAPIView)

app_name = 'Homes'

urlpatterns = [
    path('category_list', CategoryListAPIView.as_view(), name='Categories'),
    path('category_tree/<int:id>', CategoryTreeRetrieveAPIView.as_view(), name='Category Tree'),
    path('category/<int:id>', CategoryRetrieveAPIView.as_view(), name='Category'),
    path('posts_list/<id>', PostsListView.as_view(), name='Post-List'),
    path('favorite_posts', UserFavoritePostsAPIView.as_view(), name='Favorite-Post-List'),
    # path('get_search_history', GetUserSearchHistory.as_view(), name='Get-Search-History'),
    path('like/<int:post_id>', AddOrRemovePostToLikesAPIView.as_view(), name='Post-Like'),
    path('favorite/<int:post_id>', AddOrRemovePostToFavoriteAPIView.as_view(), name='Post-Favorite'),
    path('views/<int:post_id>', AddPostToViewsAPIView.as_view(), name='Post-Views'),
    path('posts_search', PostsSearchView.as_view(), name='Post-Search'),
    path('single_post/<int:pk>', PostRetrieveAPIView.as_view(), name='Post-Singe'),
    path('create_comment', CreateCommentAPIView.as_view(), name='Create-Comment'),
    path('delete_comment/<int:pk>', DeleteCommentAPIView.as_view(), name='Delete-Comment'),
    path('tags_list', TagListAPIView.as_view(), name='Tag-List'),

]
