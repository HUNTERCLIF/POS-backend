from django.urls import path
from .views import product_list, product_detail, product_create, product_update, product_delete, signup, sales_reports
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
urlpatterns = [
    path('product_list/', product_list, name='product_list'),
    path('products/<int:pk>/', product_detail, name='product_detail'),
    path('products/create/', product_create, name='product_create'),
    path('products/<int:pk>/update/', product_update, name='product_update'),
    path('products/<int:pk>/delete/', product_delete, name='product_delete'),
    path('signup/', signup, name='signup'),
    path('sales-reports/', sales_reports, name='sales_reports'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
