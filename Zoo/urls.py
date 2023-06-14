from django.urls import path

from Zoo import views
import templates



urlpatterns = [
    path('index/', views.index, name='index'),
    path('delete/<int:id>/', views.animal_delete, name='animal_delete'),
    path('login/', views.user_login, name='login'),
    path('logout/',views.logout, name='logout'),
    path('user_create/', views.user_create, name='user_create'),
    path('zone/<int:id>', views.zone, name='zone'),
    path('detail/<int:id>', views.animal_detail, name='animal_detail'),
    path('check/<int:id>', views.check, name='check'),
    path('log_delete/<int:id>/', views.log_delete, name='log_delete'),
    path('write_log/<int:id>/', views.write_log, name='write_log'),
    path('edit_log/<int:id>/', views.edit_log, name='edit_log'),
]