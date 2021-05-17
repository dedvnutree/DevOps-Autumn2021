from django.urls import path
from . import views


urlpatterns = [
    path('furniture/', views.FurnitureListView.as_view(), name='furniture'),
    path('', views.index, name='index'),
    path('furniture/<int:pk>', views.FurnitureDetailView.as_view(), name='furniture-detail'),
    path('brand/', views.BrandListView.as_view(), name='brand'),
    path('brand/<int:pk>', views.BrandDetailView.as_view(), name='brand-detail'),
    path('myaccount/', views.PersonalAccountListView.as_view(), name='my-account'),
    path('workers_page/', views.WorkersPageListView.as_view(), name='workers-page'),
    path('furniture/<uuid:pk>/renew/', views.renew_furniture_worker, name='renew-furniture-worker'),

]

urlpatterns += [
    path('furniture/create/', views.FurnitureCreate.as_view(), name='furniture-create'),
    path('furniture/<int:pk>/update/', views.FurnitureUpdate.as_view(), name='furniture-update'),
    path('furniture/<int:pk>/delete/', views.FurnitureDelete.as_view(), name='furniture-delete'),

    path('furnitureinstance/create/', views.FurnitureInstanceCreate.as_view(), name='furnitureinstance-create'),
    path('furnitureinstance/<uuid:pk>/update/', views.FurnitureInstanceUpdate.as_view(), name='furnitureinstance-update'),

    path('brand/create/', views.BrandCreate.as_view(), name='brand-create'),
    path('brand/<int:pk>/update/', views.BrandUpdate.as_view(), name='brand-update'),
    path('brand/<int:pk>/delete/', views.BrandDelete.as_view(), name='brand-delete'),
]