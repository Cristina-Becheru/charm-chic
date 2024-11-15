from django.urls import path 
from . import views


urlpatterns = [
    path('', views.view_bag, name='view_bag'),
    path('add/<item_id>/', views.add_to_bag, name='add_to_bag'),
    path('update_item/<item_id>/', views.update_item, name='update_item'),
    path('remove_item/<item_id>/', views.remove_item, name='remove_item'),
]