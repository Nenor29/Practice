from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomePage.as_view(), name="home"),
    # urls.py
    path('category/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),

    path('article/<int:id>/', views.ArticleDetail.as_view(), name="article_detail"),
    
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('signup/', views.signup_view, name="signup"),
    path('profile/', views.profile_view, name="profile"),
    path('edit_profile/', views.edit_profile, name="edit-profile"),
    
    path('category/<int:parent_id>/add/', views.category_create, name='category_create'),

    path('category/<int:id>/edit/', views.category_edit, name='category_edit'),
    path('category/<int:pk>/delete/', views.category_delete, name='category_delete'),
    
    path('article/add/<int:parent_id>/', views.article_create, name='article_create'),
    path('article/<int:pk>/delete/', views.article_delete, name='article_delete'),
    


    path('search/', views.search_results_view, name='search_results'),

    path('article/<int:pk>/update/', views.article_update_ajax, name='article_update_ajax'),


    path('article/<int:pk>/edit/', views.article_edit, name='article_edit'),
    


    
   

]