from django.urls import path, include

from . import views

app_name = 'shops'

urlpatterns = [
    # path('accounts/', include('django.contrib.auth.urls'), name = 'shop_login'),
    path('accounts/registration', views.registration, name = 'shop_registration'),
    path('account/logout', views.log_out, name = 'shop_logout'),
    path('shops/', views.index, name = 'shop_index'),
    path('create/', views.create, name = 'shop_create'),
    path('locals', views.add_local, name = 'local_create'),
    path('log_in', views.log_in, name = 'shop_login'),
    path('shops/<int:local_id>', views.local_detail, name = 'local_detail'),
    path('shops/staff', views.staff_index, name = 'staff_in_shops'),
    path('shops/staff/<int:staff_id>', views.staff_detail, name = 'staff_detail'),
    path('shops/staff/create', views.staff_create, name = 'staff_create'),




    # # Face_tracking_API
    # path('create/', views.CreateShopAPIView.as_view()),
    path('confirm/', views.confirm, name = 'shop_confirm'),
    # path('auth/', views.authenticate_user),
    # path('update/', views.ShopRetrieveUpdateAPIView.as_view()),
    # path('auth_face/', views.authenticate_face, name = 'auth_face'),
    # path('local_list/', views.get_locals_list),
    #
    # #swagger API
    # path('api/', views.schema_view),
    # # path('process/<int:user_id>', views.show, name = 'shop_destroy'),

    #test
    path('test/', views.test, name = 'test'),

]