from django.test import TestCase
from shops.models import Shops, Locals, Faces
import uuid


class ShopTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.faces = Faces.objects.create(landmarks='1234567890')
        cls.shops = Shops.objects.create(email='example@exp.com', name='example', password='123123123', shop_uuid=uuid.uuid4())
        cls.locals = cls.shops.locals_set.create(name='name')

    def setUp(self):
        shop = Shops.objects.get(email="example@exp.com")
        self.uuid = shop.shop_uuid

    def test_shops_creation(self):

        shop = Shops.objects.get(email="example@exp.com")

        self.assertEqual(shop.name, 'example')
        self.assertEqual(shop.shop_uuid, self.uuid)

    def test_shop_has_uniq_uuid(self):

        Shops.objects.create(email='exp@exp.com', name='exp', password='exp', shop_uuid=uuid.uuid4())

        shop = Shops.objects.get(email="exp@exp.com")
        self.assertNotEqual(shop.shop_uuid, self.uuid)

    def test_check_locals(self):

        count = Locals.objects.count()
        local = Locals.objects.get(shop_id=self.uuid)
        self.assertEqual(count, 1)
        self.assertEqual(local.shop.shop_uuid, self.uuid)
        self.assertEqual(local.name, 'name')

    def test_faces(self):

        f = Faces.objects.get(id = 1)
        self.assertEqual(f.id, 1)
