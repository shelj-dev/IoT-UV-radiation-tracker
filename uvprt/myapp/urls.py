from django.urls import path
from myapp import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('update_threshold/', views.update_threshold, name='update_threshold'),
    path('get-sensor/', views.get_sensor_data, name='get_sensor_data'),
]