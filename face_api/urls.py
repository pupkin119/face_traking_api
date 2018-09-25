from django.urls import path
from . import views

app_name = 'face_api'

urlpatterns = [
    # Face_tracking_API
    path('create/', views.CreateShopAPIView.as_view()),#расскомментить после деплоя
    # path('confirm/', views.confirm, name = 'shop_confirm'),
    path('auth/', views.authenticate_user),
    path('update/', views.ShopRetrieveUpdateAPIView.as_view()),
    path('auth_face/', views.authenticate_face, name = 'auth_face'),
    path('local_list/', views.get_locals_list),
    path('add_cash/', views.add_cash),
    path('face_in_shop_detail/', views.face_in_shop_detail),

    #swagger API
    # path('', views.SwaggerSchemaView.as_view()),
    # path('process/<int:user_id>', views.show, name = 'shop_destroy'),
]