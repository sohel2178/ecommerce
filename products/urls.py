from django.urls import path
from .views import ProductListView,ProductDetailView

urlpatterns = [
    path('',ProductListView.as_view(),name='product-list' ),
    path('<str:slug>/',ProductDetailView.as_view(),name='product-detail' ),
]
