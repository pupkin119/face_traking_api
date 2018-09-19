from django.test import TestCase, TransactionTestCase, SimpleTestCase
from shops.models import Shops, Locals, Faces
import uuid


class AnimalTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.faces = Faces.objects.create(landmarks='1234567890')
        cls.shops = Shops.objects.create(email='example2@exp.com', name='example', password='123123123', shop_uuid=uuid.uuid4())
        cls.locals = cls.shops.locals_set.create(name='123')

    def setUp(self):

        Shops.objects.create(email='example1@exp.com', name='example', password='123123123', shop_uuid=uuid.uuid4())
        shop = Shops.objects.get(email="example1@exp.com")

        self.uuid = shop.shop_uuid

        # Locals.objects.create(name='name', shop_id=uuid.uuid4())
    def test_animals_can_speak(self):

        shop = Shops.objects.get(email="example1@exp.com")
        self.assertEqual(shop.name, 'example')

    def test_ivalid_creation(self):

        shop = Shops.objects.get(email="example1@exp.com")
        shop.locals_set.create(name='name', shop=shop)


    def test_check_locals(self):

        count = Locals.objects.count()

        self.assertEqual(count, 1)

    def test_create_Faces(self):

        Faces.objects.create(landmarks='1234567890')

    def test_faces(self):

        f = Faces.objects.get(id = 1)
        self.assertEqual(f.id, 1)
