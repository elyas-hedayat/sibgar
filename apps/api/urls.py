from django.urls import path, include

urlpatterns = [
    path('account/', include(('apps.account.urls', "apps.account"))),
]
