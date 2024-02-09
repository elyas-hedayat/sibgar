from django.urls import path, include

from .apis import (
    ProfileDetailApi,
    ProfileListApi,

)

profile_patterns = [
    path('me/', ProfileDetailApi.as_view(), name='detail'),
    path('list/', ProfileListApi.as_view(), name='list'),
]

urlpatterns = [
    path('profile/', include((profile_patterns, 'profile'))),
]
