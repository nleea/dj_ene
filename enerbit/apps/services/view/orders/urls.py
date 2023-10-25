from django.urls import path, re_path
from .view import (
    CreateWorkOrders,
    UpdateAndDeleteWorkOrder,
    ListWorkOrdersFilter,
    RetrieveWorkOrder,
)

urlpatterns = [
    path("<int:pk>/", RetrieveWorkOrder.as_view()),
    re_path(
        r"list/(?P<status>)(?P<since>)(?P<until>)$", ListWorkOrdersFilter.as_view()
    ),
    path("create/", CreateWorkOrders.as_view()),
    path("update/<int:pk>/", UpdateAndDeleteWorkOrder.as_view()),
    path("delete/<int:pk>/", UpdateAndDeleteWorkOrder.as_view()),
]
