from django.test import TestCase

# Create your tests here.
from .models import *
from .validators import *


class CategoryTest(TestCase):
    def setUp(self) -> None:
        self.c1 = Category.objects.create(
            name='c1',
        )
        self.c2 = Category.objects.create(
            name='c2',
            parent=self.c1,
        )
        self.c3 = Category.objects.create(
            name='c3',
            parent=self.c2,
        )
        self.c4 = Category.objects.create(
            name='c4',
        )

    def test_c1_name(self):
        self.assertEqual(self.c1.name, 'c1')

    def test_c1_parent(self):
        self.assertIsNone(self.c1.parent)

    def test_c2_parent(self):
        self.assertEqual(self.c2.parent, self.c1)

    def test_c3_parent_parent(self):
        self.assertEqual(self.c3.parent.parent, self.c1)

    def test_c3_parent(self):
        self.assertEqual(self.c3.parent, self.c2)

    def test_c4_parent_parent_parent(self):
        self.c4.parent = self.c3
        self.assertEqual(self.c4.parent.parent.parent, self.c1)

    def test_c1_children(self):
        self.assertIn(self.c2, self.c1.category_set.all())

    def test_c1_children_children(self):
        self.assertIn(self.c3, self.c2.category_set.all())

    def test_delete_c1(self):
        self.c1.my_delete()
        print(self.c2.parent)
        print(Category.objects.all())
        print(Category.objects.archive())
        print(self.c2.is_deleted)
        self.assertEqual(self.c2.parent, self.c1)

    def test_delete__c1(self):
        self.c1.my_delete()
        self.assertNotIn(self.c2, Category.objects.all())

    def test_delete__c1_1(self):
        self.c1.my_delete()
        self.assertNotIn(self.c3, Category.objects.all())

    def test_delete__c1_(self):
        self.c1.my_delete()
        self.assertIn(self.c2, Category.objects.archive())

    def test_delete__c1__(self):
        self.c1.my_delete()
        print(self.c3.delete_time_stamp)
        print(self.c1.delete_time_stamp)
        print(self.c3.is_deleted)
        self.assertNotIn(self.c3, Category.objects.filter())


class DiscountTest(TestCase):
    def setUp(self) -> None:
        self.d1 = Discount.objects.create(
            is_percent=True,
            percent=70,
            max=150000,

        )
        self.d2 = Discount.objects.create(
            is_percent=False,
            price=30000,
            max=150000,
        )
        self.d3 = Discount.objects.create(
            is_percent=True,
            percent=22.5,
            max=150000,

        )
        self.d4 = Discount.objects.create(
            price=10500,
            max=150000,
        )
        self.d5 = Discount.objects.create(
            price=10000,
        )

    def test_d1(self):
        self.assertEqual(self.d1.percent, 70)
        self.assertEqual(self.d1.price, 0)
        self.assertEqual(self.d1.max, 150000)
        self.assertIsNone(self.d1.delete_time_stamp)
        self.assertFalse(self.d1.is_deleted)
        print(self.d1.is_deleted)
        self.assertFalse(self.d1.is_expired())
        print(self.d1.is_expired())

    def test_d2(self):
        self.assertEqual(self.d2.percent, 0)
        self.assertEqual(self.d2.price, 30000)
        self.assertEqual(self.d2.max, 150000)

    def test_delete_discount(self):
        self.d1.my_delete()
        self.assertIsNotNone(self.d1.delete_time_stamp)
        self.assertTrue(self.d1.is_deleted)
        self.assertTrue(self.d1.is_expired())

    def test_final_price_percent(self):
        self.assertEqual(self.d1.final_price(100), 30)

    def test_final_price_percent_big(self):
        self.assertEqual(self.d1.final_price(1000000), 850000)

    def test_final_price_price(self):
        self.assertEqual(self.d2.final_price(40000), 10000)

    def test_final_price_price_big(self):
        self.assertRaises(AssertionError, self.d2.final_price, 29000)

    def test_d4(self):
        self.assertEqual(self.d4.percent, 0)
        self.assertEqual(self.d4.price, 10500)

    def test_d3(self):
        self.assertEqual(self.d3.percent, 22.5)
        self.assertEqual(self.d3.price, 0)
        self.assertEqual(self.d3.final_price(100), 78)
        print(self.d3.final_price(100))

    def test_d5(self):
        self.assertEqual(self.d5.percent, 0)
        self.assertEqual(self.d5.price, 10000)
        self.assertEqual(self.d5.max, None)
        self.assertEqual(self.d5.final_price(11000), 1000)
        self.assertRaises(AssertionError, self.d5.final_price, 900)


class PercentValidatorTest(TestCase):
    def test_value_neg1(self):
        self.assertRaises(ValidationError, percent_validator, -1)

    def test_value_120(self):
        self.assertRaises(ValidationError, percent_validator, 120)

    def test_value_neg_5(self):
        self.assertRaises(ValidationError, percent_validator, -5)

    def test_value_101(self):
        self.assertRaises(ValidationError, percent_validator, 101)


class PriceValidatorTest(TestCase):
    def test_value_neg1(self):
        self.assertRaises(ValidationError, price_validator, -1)

    def test_value_neg_100(self):
        self.assertRaises(ValidationError, price_validator, -100)
