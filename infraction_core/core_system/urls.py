from django.urls import path
from . import views

urlpatterns = [
    path('comparendos/', views.Fotomultas.as_view(), name='comparendos'),
    path('personas/', views.Personas.as_view(), name='personas'),
]