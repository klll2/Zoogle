from django.urls import path

from Zoo import views
import templates



urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/',views.logout, name='logout'),
    path('user_create/', views.user_create, name='user_create'),
    path('index/', views.index, name='index'),
    path('detail/<int:id>', views.animal_detail, name='animal_detail'),
    path('animal_delete/<int:id>/', views.animal_delete, name='animal_delete'),
    path('check/<int:id>', views.check, name='check'),
    path('search/', views.search, name='search'),
    path('search_filter/', views.search_filter, name='search_filter'),
    path('write_log/<int:id>/', views.write_log, name='write_log'),
    path('edit_log/<int:id>/', views.edit_log, name='edit_log'),
    path('log_delete/<int:id>/', views.log_delete, name='log_delete'),
    path('zone/<int:id>', views.zone, name='zone'),
]