from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.core.cache import cache
from .models import Profile
from .selectors import profile_list, get_profile
from ..api.mixins import ApiAuthMixin
from ..api.pagination import LimitOffsetPagination, get_paginated_response_context

user = get_user_model()


class ProfileListApi(ApiAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

    class ProfileListSerializer(serializers.ModelSerializer):
        user_id = serializers.IntegerField(source="user.id")
        email = serializers.EmailField(source="user.email")

        class Meta:
            model = Profile
            fields = ("user_id", "email", "id", "first_name", "last_name", "age", "gender", "starting_date")

    @extend_schema(
        responses={status.HTTP_200_OK: ProfileListSerializer},
        description="List All Users Profile"
    )
    def get(self, request):
        query = profile_list()
        return get_paginated_response_context(
            pagination_class=self.Pagination,
            serializer_class=self.ProfileListSerializer,
            queryset=query,
            request=request,
            view=self,
        )


class ProfileDetailApi(ApiAuthMixin, APIView):
    class ProfileDetailSerializer(serializers.ModelSerializer):
        user_id = serializers.IntegerField(source="user.id")
        email = serializers.EmailField(source="user.email")

        class Meta:
            model = Profile
            fields = ("user_id", "email", "id", "first_name", "last_name", "age", "gender", "starting_date")

    @extend_schema(
        responses={status.HTTP_200_OK: ProfileDetailSerializer},
        description="Return Requested User Profile"
    )
    def get(self, request):
        query = get_profile(_user=request.user)

        data = self.ProfileDetailSerializer(query).data

        return Response(data, status=status.HTTP_200_OK)


class AccountRegisterOtpApi(APIView):
    class RegisterInputSerializer(serializers.Serializer):
        phone_number = serializers.CharField(max_length=11, )  # todo:add validators

        def validate_phone_number(self, phone_number):
            if user.objects.filter(phone_number=phone_number).exists():
                raise serializers.ValidationError("phone_number already exists")
            return phone_number

    @extend_schema(request=RegisterInputSerializer, description="Send Otp For Registration Of User")
    def post(self, request):
        serializer = self.RegisterInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # cache.set()
        # send_otp.dealy()
        return Response(data={"message": "otp sent"}, status=status.HTTP_200_OK)


class AccountVerifyRegisterApi(APIView):
    class VerifyRegisterInputSerializer(serializers.Serializer):
        phone_number = serializers.CharField(max_length=11, )
        code = serializers.CharField(max_length=6)

    @extend_schema(request=VerifyRegisterInputSerializer, description="Verify That User Enter Valid Otp Code or Not")
    def post(self, request):
        serializer = self.VerifyRegisterInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cache.get()  # todo:
        # send_otp.dealy()
        return Response(data={"message": "otp sent"}, status=status.HTTP_200_OK)


class ChangePasswordApi(ApiAuthMixin, APIView):
    class ChangePasswordSerializer(serializers.Serializer):
        old_password = serializers.CharField(max_length=10, )
        new_password = serializers.CharField(max_length=10, )
        confirm_password = serializers.CharField(max_length=10, )

        def validate(self, data):
            if not self.request.user.check_password(data.get("old_passw")):
                return serializers.ValidationError("old password is not valid.")
            if data.get("old_password") == data.get("new_password"):
                return serializers.ValidationError("old password and new password can not be same.")
            if data.get("new_password") != data.get("confirm_password"):
                raise serializers.ValidationError("confirm password is not equal to password")
            return data

    @extend_schema(request=ChangePasswordSerializer, description="Change user password into new password")
    def post(self, request):
        serializer = self.ChangePasswordSerializer(data=request.data, context={"request": self.request})
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data.get("new_password"))
        return Response(data={"message": "password change successfully"}, status=status.HTTP_200_OK)


class ForgetPasswordSendOtpApi(APIView):
    class ForgetPasswordSendOtpSerializer(serializers.Serializer):
        phone_number = serializers.CharField(max_length=11)  # todo:set regax for this

        def validate_phone_number(self, phone_number):
            if not user.objects.filter(phone_number=phone_number).exists():
                raise serializers.ValidationError("phone_number  dose not exists")
            return phone_number

    @extend_schema(request=ForgetPasswordSendOtpSerializer, description="Send otp for forget password")
    def post(self, request):
        serializer = self.ForgetPasswordSendOtpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # todo: implement ologic
        return Response(data={"message": "message sent to your phone_number for forget password"},
                        status=status.HTTP_200_OK)
