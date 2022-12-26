from django.urls import path
from views import Fotomultas
from views import MultasTuio

urlpatterns = [
    path('comparendos/', Fotomultas.Fotomultas.as_view(), name='comparendos'),
    path('multas-tuio/', MultasTuio.MultasTuio.as_view(), name='multas-tuio'),
    path('cron-multas-tuio/', MultasTuio.CronMultasTuio.as_view(), name='cron-multas-tuio'),
]