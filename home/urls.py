from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('admin', admin.site.urls),  # ✅ Ensure admin panel is accessible

    # Authentication
    path('', views.user_login, name='login'),
    
    # Home & General Pages
    path('home/', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),

    # Blog URLs
    path('blog/', views.blog, name='blog'),
    path('blog/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('blog/create/', views.blog_create, name='blog_create'),
    path('blog/update/<int:pk>/', views.blog_update, name='blog_update'),
    path('blog/delete/<int:pk>/', views.blog_delete, name='blog_delete'),

    # Category Filtering
    path('category/<str:category>/', views.category_posts, name='category_posts'),
]
