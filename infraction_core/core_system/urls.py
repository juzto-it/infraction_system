from django.urls import path
from . import views

urlpatterns = [
    path('comparendos/', views.Fotomultas.as_view(), name='comparendos'),
    path('consultas/', views.Consultas.as_view(), name='consultas'),
]