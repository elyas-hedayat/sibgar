from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Profile
from .selectors import profile_list, get_profile
from ..api.mixins import ApiAuthMixin
from ..api.pagination import LimitOffsetPagination, get_paginated_response_context


class ProfileListApi(ApiAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class OutPutSerializer(serializers.ModelSerializer):
        user_id = serializers.IntegerField(source="user.id")
        email = serializers.EmailField(source="user.email")

        class Meta:
            model = Profile
            fields = ("user_id", "email", "id", "first_name", "last_name", "age", "gender", "starting_date")

    @extend_schema(
        responses={status.HTTP_200_OK: OutPutSerializer},
        description="List All Users Profile"
    )
    def get(self, request):
        query = profile_list()

        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=self.OutPutSerializer,
            queryset=query,
            request=request,
            view=self,
        )


class ProfileDetailApi(ApiAuthMixin, APIView):
    class OutPutSerializer(serializers.ModelSerializer):
        user_id = serializers.IntegerField(source="user.id")
        email = serializers.EmailField(source="user.email")

        class Meta:
            model = Profile
            fields = ("user_id", "email", "id", "first_name", "last_name", "age", "gender", "starting_date")

    @extend_schema(
        responses={status.HTTP_200_OK: OutPutSerializer},
        description="Return Requested User Profile"
    )
    def get(self, request):
        query = get_profile(_user=request.user)

        data = self.OutPutSerializer(query).data

        return Response(data, status=status.HTTP_200_OK)
