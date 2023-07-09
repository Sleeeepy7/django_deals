from django.urls import path
from .views import DealUploadView, TopCustomersView

urlpatterns = [
    path('upload_file/', DealUploadView.as_view(), name="upload_file"),
    path('top_customers/', TopCustomersView.as_view(), name="top_customers")
]
