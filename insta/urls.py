"""
URL configuration for insta project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from app1.views import home1,register,profile,user_login,user_logout,home,create_post,post_detail,edit_post,delete_post,user_posts,like_post,share_post
from app1.views import user_profile,follow_user,explore_users,create_story,story_detail,delete_story,search,all_stories,inbox,conversation,new_conversation,load_messages
urlpatterns = [
    path('admin/', admin.site.urls),
    path('home1',home1,name="home1"),
    path('',home,name="home"),
    path('register',register,name='register'),
    path('profile/',profile,name='profile'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),

    # path('all_post',all_post,name="all_post"),
    # path('create_post',create_post,name="create_post"),

    path('create/', create_post, name='create_post'),
    path('create/', create_post, name='create_post'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('post/<int:pk>/edit/', edit_post, name='edit_post'),
    path('post/<int:pk>/delete/', delete_post, name='delete_post'),
    path('my-posts/', user_posts, name='user_posts'),

   path('create/', create_post, name='create_post'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('post/<int:pk>/like/', like_post, name='like_post'),
    path('post/<int:pk>/share/', share_post, name='share_post'),
    path('user/<str:username>/', user_profile, name='user_profile'),
    path('user/<str:username>/follow/', follow_user, name='follow_user'),
    path('explore/',explore_users, name='explore_users'),

    path('create_story/', create_story, name='create_story'),
    path('stories/', all_stories, name='all_stories'),
    path('story/<int:pk>/',story_detail, name='story_detail'),
    path('story/<int:pk>/delete/',delete_story, name='delete_story'),
    path('search/', search, name='search'),


    path('inbox/', inbox, name='inbox'),
    path('conversation/<int:conversation_id>/', conversation, name='conversation'),
    path('new_conversation/<str:username>/', new_conversation, name='new_conversation'),
    path('load_messages/<int:conversation_id>/', load_messages, name='load_messages'),



]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


    #  Gayle+333