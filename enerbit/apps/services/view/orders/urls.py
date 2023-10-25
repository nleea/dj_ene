from django.urls import path, re_path
from .view import (
    CreateWorkOrders,
    UpdateWorkOrder,
    DeleteWorkOrder,
    ListWorkOrdersFilter,
    RetrieveWorkOrder,
)

app_name = "work-orders"

urlpatterns = [
    path("<int:pk>/", RetrieveWorkOrder.as_view(), name="work-orders-by-pk"),
    re_path(
        r"list/(?P<status>)(?P<since>)(?P<until>)$", ListWorkOrdersFilter.as_view(),name="work-orders-filter"
    ),
    path("create/", CreateWorkOrders.as_view(),name="work-orders-create"),
    path("update/<int:pk>/", UpdateWorkOrder.as_view(),name="work-orders-update"),
    path("delete/<int:pk>/", DeleteWorkOrder.as_view(),name="work-orders-delete"),
]
