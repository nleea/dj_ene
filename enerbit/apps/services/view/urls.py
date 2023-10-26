from django.urls import path, include

urlpatterns = [
    path("customer/", include("apps.services.view.customer.urls")),
    path("orders/", include("apps.services.view.orders.urls")),
]
