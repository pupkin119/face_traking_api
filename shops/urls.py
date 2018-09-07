from django.urls import path, include

from . import views

app_name = 'shops'

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('shops/', views.index, name = 'shop_index'),
    path('create/', views.create, name = 'shop_create'),
    # path('process/<int:user_id>', views.show, name = 'shop_destroy'),
]