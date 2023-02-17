from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)

from user.views import UserRegister

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include([
        path('v1/', include([
            path('auth/', include([
                path('sign-in/', TokenObtainPairView.as_view(),
                     name='sign_in'),
                path('sign-up/', UserRegister.as_view()),
                path('refresh-token/', TokenRefreshView.as_view(),
                     name='refresh_token'),
            ])),
            path('advertising/', include('advertising.urls'))
        ]))
    ])),
]
