from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    UpdateAPIView,
    DestroyAPIView,
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


class CreateCustomer(CreateAPIView):
    serializer_class = CustomerSerializer

    def create(self, request, *args, **kwargs):
        body = request.data

        serializer = self.serializer_class(data=body)

        if not serializer.is_valid():
            return Response(
                {
                    "errors": serializer.errors,
                    "status": status.HTTP_400_BAD_REQUEST,
                    "valid": False,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            serializer.save()
            return Response(
                {"message": "Ok", "status": status.HTTP_200_OK, "valid": True},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {
                    "errors": e.args,
                    "status": status.HTTP_400_BAD_REQUEST,
                    "valid": False,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class ListCustomer(ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializerList

    def get_queryset(self):
        active = re.match(".*/active/?", self.request.get_full_path())

        if active:
            return Customer.objects_filters.filterByStatus()

        return super().get_queryset()


class UpdateAndDeleteCustomer(UpdateAPIView, DestroyAPIView):
    serializer_class = CustomerSerializerUpdate

    def get_object(self) -> Customer | None:
        try:
            pk = self.kwargs.get("pk")
            if pk:
                return Customer.objects.get(pk=pk)
            return None
        except Customer.DoesNotExist:
            return None

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if not instance:
            return Response(
                {
                    "errors": "This customer don't exist",
                    "status": status.HTTP_400_BAD_REQUEST,
                    "valid": False,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = request.data

        serializer = self.serializer_class(instance=instance, data=data, partial=True)

        if not serializer.is_valid():
            return Response(
                {
                    "errors": serializer.errors,
                    "status": status.HTTP_400_BAD_REQUEST,
                    "valid": False,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            serializer.save()
            return Response(
                {"message": "Ok", "status": status.HTTP_200_OK, "valid": True},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {
                    "errors": e.args,
                    "status": status.HTTP_400_BAD_REQUEST,
                    "valid": False,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()

        if not instance:
            return Response(
                {
                    "errors": "This customer don't exist",
                    "status": status.HTTP_400_BAD_REQUEST,
                    "valid": False,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            instance.delete()
            return Response(
                {"message": "Ok", "status": status.HTTP_200_OK, "valid": True},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {
                    "errors": e.args,
                    "status": status.HTTP_400_BAD_REQUEST,
                    "valid": False,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
