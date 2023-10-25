from django.urls import path
from .view import (
    CreateCustomer,
    ListCustomer,
    UpdateCustomer,
    DeleteCustomer,
    RetrieveCustomer,
)

app_name = "customer"

urlpatterns = [
    path("list/", ListCustomer.as_view(), name="customer-list"),
    path("list/active/", ListCustomer.as_view(), name="customer-active"),
    path("<int:pk>/", RetrieveCustomer.as_view(), name="customer-id"),
    path("create/", CreateCustomer.as_view(), name="customer-create"),
    path("update/<int:pk>/", UpdateCustomer.as_view(), name="customer-update"),
    path("delete/<int:pk>/", DeleteCustomer.as_view(), name="customer-delete"),
]
