"""GameCave URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from GamersCave import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage),
    path('add_user/', views.RegisterUserView.as_view()),
    path('user/<int:user_id>/', views.UserView.as_view()),
    path('login/', views.LoginUserView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('add_studio/', views.AddStudioView.as_view()),
    path('studio/<int:studio_id>/', views.StudioView.as_view()),
    path('all_studios/', views.AllStudioView.as_view()),
    path('add_game/', views.AddGameView.as_view()),
    path('game/<int:game_id>/', views.GameView.as_view()),
    path('all_games/', views.AllGameView.as_view()),
    path('add_article/', views.AddArticleView.as_view()),
    path('all_articles/', views.AllArticleView.as_view()),
    path('gamecave/forum/', views.ForumView.as_view()),
    path('gamecave/forum/addpost/', views.ForumPostAddView.as_view()),
    path('gamecave/forum/<int:forum_post_id>/', views.ForumPostView.as_view()),


]
