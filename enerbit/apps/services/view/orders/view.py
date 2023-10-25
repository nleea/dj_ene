from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.response import Response
from rest_framework import status
from ...serializers.servicies.serializers_services import (
    WorkOrderSerializer,
    WorkOrderSerializerList,
    WorkOrderSerializerUpdate,
)
from ...models import WorkOrder
from ...mixins.base import MemberMixin
import datetime


class CreateWorkOrders(MemberMixin, CreateAPIView):
    serializer_class = WorkOrderSerializer

    def create(self, request, *args, **kwargs):
        body = request.data

        serializer = self.serializer_class(data=body)
        self.meta_data = "POST"

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
            self.data = {"message": "Ok", "status": status.HTTP_200_OK, "valid": True}
            return Response(
                self.response_obj,
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


class RetrieveWorkOrder(MemberMixin, ListAPIView):
    serializer_class = WorkOrderSerializerList

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk",None)

        queryset = WorkOrder.objects.filter(pk=pk).select_related("customer")

        serializer = self.serializer_class(queryset, many=True)

        self.data = serializer.data
        self.meta_data = "GET"
        self.module = "WorkOrders"

        return Response(self.response_obj, status=status.HTTP_200_OK)


class ListWorkOrdersFilter(MemberMixin, ListAPIView):
    serializer_class = WorkOrderSerializerList

    def validate_date(self, since, until):
        try:
            datetime.datetime.strptime(since, "%Y-%m-%d")
            datetime.datetime.strptime(until, "%Y-%m-%d")
            return True
        except Exception:
            return False

    def get_queryset(self):
        since = self.request.GET.get("since", None)
        until = self.request.GET.get("until", None)
        status = self.request.GET.get("status", None)

        if since and until:
            if self.validate_date(since, until):
                return WorkOrder.objects_filters.filterByDate(since, until)
            return None
        elif status:
            return WorkOrder.objects_filters.filterByState(status)

        return WorkOrder.objects.all().select_related("customer")

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(), many=True)

        self.data = serializer.data
        self.meta_data = "GET"
        self.module = "ListWorkOrders"

        return Response(self.response_obj, status=status.HTTP_200_OK)


class UpdateAndDeleteWorkOrder(MemberMixin, UpdateAPIView, DestroyAPIView):
    serializer_class = WorkOrderSerializerUpdate

    def get_object(self) -> WorkOrder | None:
        try:
            pk = self.kwargs.get("pk")
            if pk:
                return WorkOrder.objects.get(pk=pk)
            return None
        except WorkOrder.DoesNotExist:
            return None

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        self.meta_data = "PUT"
        if not instance:
            self.error = (
                {
                    "errors": "This order don't exist",
                    "status": status.HTTP_400_BAD_REQUEST,
                    "valid": False,
                },
            )
            return Response(
                self.response_obj,
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = request.data

        serializer = self.serializer_class(instance=instance, data=data, partial=True)

        if not serializer.is_valid():
            self.error = (
                {
                    "errors": serializer.errors,
                    "status": status.HTTP_400_BAD_REQUEST,
                    "valid": False,
                },
            )

            return Response(
                self.response_obj,
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            serializer.save()
            self.data = {"message": "Ok", "status": status.HTTP_200_OK, "valid": True}
            return Response(
                self.response_obj,
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            self.data = {
                "errors": e.args,
                "status": status.HTTP_400_BAD_REQUEST,
                "valid": False,
            }

            return Response(
                self.response_obj,
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.meta_data = "DELETE"

        if not instance:
            self.error = (
                {
                    "errors": "This order don't exist",
                    "status": status.HTTP_400_BAD_REQUEST,
                    "valid": False,
                },
            )

            return Response(
                self.response_obj,
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            instance.delete()
            self.data = {"message": "Ok", "status": status.HTTP_200_OK, "valid": True}
            return Response(
                self.response_obj,
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            self.data = {
                "errors": e.args,
                "status": status.HTTP_400_BAD_REQUEST,
                "valid": False,
            }

            return Response(
                self.response_obj,
                status=status.HTTP_400_BAD_REQUEST,
            )
