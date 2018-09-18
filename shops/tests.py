from django.test import TestCase
from shops.models import Shops
import uuid


class ShopModelTests(TestCase):

    def setUp(self):
        Shops.objects.create(email='example@exp.com', name='example', password='123123123')
        Shops.objects.create(email='example1@exp.com', name='example', password='123123123')

    def test_shops_responce_tocreation(self):
        shop = Shops.objects.get(email='example@exp.com')
        self.assertEqual(shop.password, '123123123')
        self.assertEqual(shop.email, 'example@exp.com')
        self.assertEqual(shop.name, 'example')

    def uniq_shops_uuid(self):
        shop1 = Shops.objects.get(email='example@exp.com')
        shop2 = Shops.objects.get(email='example1@exp.com')

        self.assertNotEqual(shop1.shop_uuid, shop2.shop_uuid)


#
#
#
# class QuestionIndexViewTests(TestCase):
#     def test_no_questions(self):
#         """
#         If no questions exist, an appropriate message is displayed.
#         """
#         response = self.client.get(reverse('polls:index'))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, "No polls are available.")
#         self.assertQuerysetEqual(response.context['latest_question_list'], [])
#
#
# class AnimalTestCase(TestCase):
#     def setUp(self):
#         Animal.objects.create(name="lion", sound="roar")
#         Animal.objects.create(name="cat", sound="meow")
#
#     def test_animals_can_speak(self):
#         """Animals that can speak are correctly identified"""
#         lion = Animal.objects.get(name="lion")
#         cat = Animal.objects.get(name="cat")
#         self.assertEqual(lion.speak(), 'The lion says "roar"')
#         self.assertEqual(cat.speak(), 'The cat says "meow"')

# class QuestionModelTests(TestCase):
#
#     def test_was_published_recently_with_future_question(self):
#         """
#         was_published_recently() returns False for questions whose pub_date
#         is in the future.
#         """
#         time = timezone.now() + datetime.timedelta(days=30)
#         future_question = Question(pub_date=time)
#         self.assertIs(future_question.was_published_recently(), False)
