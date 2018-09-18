# from django.test import TestCase
# from shops.models import Shops
#
#
# class ShopModelTests(TestCase):
#
#     def setUp(self):
#         Shops.objects.create(email='example@exp.com', name='example', password='123123123')
#         Shops.objects.create(email='example1@exp.com', name='example', password='123123123')
#
#     def test_shops_responce_tocreation(self):
#         shop = Shops.objects.get(email='example@exp.com')
#         self.assertEqual(shop.password, '123123123')
#         self.assertEqual(shop.email, 'example@exp.com')
#         self.assertEqual(shop.name, 'example')
#
#     def uniq_shops_uuid(self):
#         shop1 = Shops.objects.get(email='example@exp.com')
#         shop2 = Shops.objects.get(email='example1@exp.com')
#
#         self.assertNotEqual(shop1.shop_uuid, shop2.shop_uuid)