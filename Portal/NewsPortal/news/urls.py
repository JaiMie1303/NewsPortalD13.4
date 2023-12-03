from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('', NewsList.as_view(), name='news_list'),
    path('<int:pk>', PostDetailView.as_view(), name='post_detail'),
    path('search/', SearchPost.as_view(), name='postsearch'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('subscriptions/', subscriptions, name='subscriptions'),
]