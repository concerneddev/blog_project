from django.urls import path
from . import views
from .feeds import LatestPostsFeed


#application-namespace, allows you to organize URLs by application
app_name = 'blog'

'''ch2 SEO friendly URLs 
    we modify the path from 
    <int:id>
    to
    <int:year>/<int:month>/<int:day>/<slug:post>/
    '''
urlpatterns = [
    #Post views
    path('', views.post_list, name='post_list'),
    #path('',views.PostListView.as_view(),name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/',views.post_share, name='post_share'),
    path('<int:post_id>/comment/',views.post_comment, name='post_comment'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('search/', views.post_search, name='post_search'),
]