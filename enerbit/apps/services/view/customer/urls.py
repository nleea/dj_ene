from django.urls import path, re_path
from .view import (
    CreateCustomer,
    ListCustomer,
    UpdateAndDeleteCustomer,
    
)

urlpatterns = [
    path("list/", ListCustomer.as_view()),
    path("list/active/", ListCustomer.as_view()),
    path("create/", CreateCustomer.as_view()),
    path("update/<int:pk>/", UpdateAndDeleteCustomer.as_view()),
    path("delete/<int:pk>/", UpdateAndDeleteCustomer.as_view()),
]
