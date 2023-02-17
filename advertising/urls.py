from django.urls import path

from advertising.views import AdvertisingAPIView, UpdateStatusAdvertisingAPIView

urlpatterns = [
    path('', AdvertisingAPIView.as_view(), name='advertising-create'),
    path('change-status/', UpdateStatusAdvertisingAPIView.as_view(),
         name='change-status')
]
