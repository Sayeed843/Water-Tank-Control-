from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'wpc'
urlpatterns = [
    path('index/', views.index, name='main-view'),
    path('motor_status/', views.motor_status, name='motorStatus'),
    path('about_me/', views.about_me, name='about_me'),
    path('motor_status/<int:user_id>/', views.motor_details, name='motor_details'),
    path('motor_status/<int:user_id>/decision/', views.decision, name='decision'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
