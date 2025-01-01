"""
URL configuration for blogs project.

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
from blog import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index, name="index" ),
    path('signup/',views.signup, name="signup" ),
    path('save_user/',views.save_user),
    path('login_page/',views.login_page),
    path('blogs/', views.blog_list, name='blog_list'),
    path('blog/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('blog/<int:blog_id>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/like/', views.like_comment, name='like_comment'),
    path('blog/share/<int:blog_id>/', views.share_blog, name='share_blog'),
    path('logout/', views.logout_view, name='logout'),
    # path('blog/like/<int:blog_id>/', views.like_blog, name='like_blog'),
    path('blog/search/', views.combined_blog_search, name='combined_blog_search'),
    # path('similar-search/', views.similar_blog_search, name='similar_blog_search'),
    # path('tag_search/', views.tag_search, name='tag_search'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)