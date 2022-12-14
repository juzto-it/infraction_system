from django.urls import path
from . import views

urlpatterns = [
    path('comparendos/', views.Fotomultas.as_view(), name='comparendos'),
    path('multas-tuio/', views.MultasTuio.as_view(), name='multas-tuio'),
]