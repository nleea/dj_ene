from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    UpdateAPIView,
    DestroyAPIView,
    RetrieveAPIView,
)
from rest_framework.response import Response
from rest_framework import status
from ...serializers.customers.serializers_customers import (
    CustomerSerializer,
    CustomerSerializerUpdate,
    CustomerSerializerList,
)
from ...models import Customer
import re
from ...mixins.base import MemberMixin


class CreateCustomer(CreateAPIView, MemberMixin):
    serializer_class = CustomerSerializer

    def create(self, request, *args, **kwargs):
        self.meta_data = "POST"

        body = request.data

        serializer = self.serializer_class(data=body)

        if not serializer.is_valid():
            self.error = {
                "errors": serializer.errors,
                "status": status.HTTP_400_BAD_REQUEST,
                "valid": False,
            }

            return Response(
                self.response_obj,
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            serializer.save()
            self.data = {
                "message": "Ok",
                "status": status.HTTP_200_OK,
                "valid": True,
            }
            return Response(
                self.response_obj,
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            self.error = {
                "errors": e.args,
                "status": status.HTTP_400_BAD_REQUEST,
                "valid": False,
            }

            return Response(
                self.response_obj,
                status=status.HTTP_400_BAD_REQUEST,
            )


class RetrieveCustomer(MemberMixin, RetrieveAPIView):
    serializer_class = CustomerSerializerList

    def get_queryset(self):
        pk = self.kwargs.get("pk", None)
        return Customer.objects_filters.filterById(pk)

    def get(self, request, *args, **kwargs):
        self.meta_data = "GET"

        queryset = self.get_queryset()
        serializers = self.serializer_class(queryset, many=True)

        self.data = serializers.data

        return Response(self.response_obj, status=status.HTTP_200_OK)


class ListCustomer(MemberMixin, ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializerList

    def get_queryset(self):
        active = re.match(r".*/active/?", self.request.get_full_path())

        if active:
            return Customer.objects_filters.filterByStatus()

        return super().get_queryset()

    def get(self, request, *args, **kwargs):
        self.meta_data = "GET"

        queryset = self.get_queryset()

        serializer = self.serializer_class(
            queryset, many=True, context={"orders": True}
        )

        self.data = serializer.data

        return Response(self.response_obj, status=status.HTTP_200_OK)


class UpdateCustomer(UpdateAPIView, MemberMixin):
    serializer_class = CustomerSerializerUpdate

    def get_queryset(self):
        try:
            pk = self.kwargs.get("pk")
            if pk:
                return Customer.objects.get(pk=pk)
            return None
        except Customer.DoesNotExist:
            return None

    def update(self, request, *args, **kwargs):
        self.meta_data = "PUT"
        instance = self.get_queryset()

        if not instance:
            self.error = {
                "errors": "This customer don't exist",
                "status": status.HTTP_400_BAD_REQUEST,
                "valid": False,
            }

            return Response(
                self.error,
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = request.data

        serializer = self.serializer_class(instance=instance, data=data, partial=True)

        if not serializer.is_valid():
            self.error = {
                "errors": serializer.errors,
                "status": status.HTTP_400_BAD_REQUEST,
                "valid": False,
            }

            return Response(
                self.error,
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            serializer.save()
            self.data = {
                "message": "Ok",
                "status": status.HTTP_200_OK,
                "valid": True,
            }
            return Response(
                self.response_obj,
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            self.error = {
                "errors": e.args,
                "status": status.HTTP_400_BAD_REQUEST,
                "valid": False,
            }

            return Response(
                self.response_obj,
                status=status.HTTP_400_BAD_REQUEST,
            )


class DeleteCustomer(DestroyAPIView, MemberMixin):
    def get_queryset(self):
        try:
            pk = self.kwargs.get("pk")
            if pk:
                return Customer.objects.get(pk=pk)
            return None
        except Customer.DoesNotExist:
            return None

    def delete(self, request, *args, **kwargs):
        self.meta_data = "Delete"
        instance = self.get_object()

        if not instance:
            self.error = {
                "errors": "This customer don't exist",
                "status": status.HTTP_400_BAD_REQUEST,
                "valid": False,
            }

            return Response(
                self.error,
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            instance.delete()
            self.data = {
                "message": "Ok",
                "status": status.HTTP_200_OK,
                "valid": True,
            }
            return Response(
                self.response_obj,
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            self.error = {
                "errors": e.args,
                "status": status.HTTP_400_BAD_REQUEST,
                "valid": False,
            }

            return Response(
                self.error,
                status=status.HTTP_400_BAD_REQUEST,
            )
