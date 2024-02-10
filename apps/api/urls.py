from django.urls import path, include

urlpatterns = [
    path('account/', include(('apps.account.urls', "apps.account"))),
    path('auth/', include(('apps.authentication.urls', "apps.authentication"))),
]
