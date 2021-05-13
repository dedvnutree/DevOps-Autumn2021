from django.urls import path
from . import views


urlpatterns = [
    path('furniture/', views.FurnitureListView.as_view(), name='furniture'),
    path('', views.index, name='index'),
    path('furniture/<int:pk>', views.FurnitureDetailView.as_view(), name='furniture-detail'),
    path('brand/', views.BrandListView.as_view(), name='brand'),
    path('brand/<int:pk>', views.BrandDetailView.as_view(), name='brand-detail'),
    path('myfurniture/', views.ReservedFurnitureByUserListView.as_view(), name='my-reserved'),
]