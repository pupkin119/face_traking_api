# from rest_framework import serializers
# from shops.models import Shops, Faces_in_shops, Locals
# from django.contrib.auth.hashers import make_password, Argon2PasswordHasher
#
#
# class ShopSerializer(serializers.ModelSerializer):
#     # date_joined = serializers.ReadOnlyField()
#
#     def create(self, validated_data):
#         shop = Shops(
#             email=validated_data['email'],
#         )
#         shop.set_password(validated_data['password'])
#         shop.save()
#         return shop
#
#     class Meta(object):
#         model = Shops
#         fields = ('id', 'email', 'password', 'shop_uuid', 'is_active')
#
#
# class FacesInShopSerializer(serializers.ModelSerializer):
#     class Meta(object):
#         model = Faces_in_shops
#         fields = ()
#
#
# class LocalsSerializer(serializers.ModelSerializer):
#     class Meta(object):
#         model = Locals
#         fields = ('id', 'name')
#
# class FacesInShopDetailSerializer(serializers.ModelSerializer):
#     class Meta(object):
#         model = Faces_in_shops
#         fields = ('face_id', 'local_id', 'counts', 'time')
