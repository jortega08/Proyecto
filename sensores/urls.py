from django.urls import path
from . import views
from .api import SensorDataReceiver, BatteryDataReceiver, CurrentDataReceiver
urlpatterns = [
    path('api/sensores/receive/', SensorDataReceiver.as_view(), name='sensor_data_receiver'),
    path('api/sensores/battery/', BatteryDataReceiver.as_view(), name='battery_data_receiver'),
    path('api/sensores/current/', CurrentDataReceiver.as_view(), name='current_data_receiver'),
    path('api/led-control/', views.control_leds, name='control_leds'),
    path('led-control/', views.led_control_page, name='led_control_page'),
    path('battery_data/', views.battery_data_view, name='battery_data_view'),
    path('current_data/', views.current_data_view, name='current_data_view'),
    path('battery_status/', views.battery_status, name='battery_status'),
]
