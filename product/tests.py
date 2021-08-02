from datetime import timedelta

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
            expire_date_time=timezone.now() + timedelta(days=5),

        )
        self.d2 = Discount.objects.create(
            is_percent=False,
            price=30000,
            max=150000,
            expire_date_time=timezone.now() + timedelta(days=5),
        )
        self.d3 = Discount.objects.create(
            is_percent=True,
            percent=22.5,
            max=150000,
            expire_date_time=timezone.now() + timedelta(days=5),

        )
        self.d4 = Discount.objects.create(
            price=10500,
            max=150000,
            expire_date_time=timezone.now() + timedelta(days=5),
        )
        self.d5 = Discount.objects.create(
            price=10000,
            expire_date_time=timezone.now() - timedelta(days=5),
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
        self.assertTrue(self.d5.is_expired())


class OffCodeTest(TestCase):
    def setUp(self) -> None:
        self.o1 = OffCode.objects.create(
            is_percent=True,
            percent=70,
            max=150000,
            code='off70',
            expire_date_time=timezone.now() + timedelta(days=5),
        )
        self.o2 = OffCode.objects.create(
            is_percent=False,
            price=30000,
            max=150000,
            code='tabestan400',
            expire_date_time=timezone.now() + timedelta(days=5),
        )
        self.o3 = OffCode.objects.create(
            is_percent=True,
            percent=22.5,
            max=150000,
            code='paeiz',
            expire_date_time=timezone.now() + timedelta(days=5),
        )
        self.o4 = OffCode.objects.create(
            price=10500,
            max=150000,
            code='test',
            expire_date_time=timezone.now() - timedelta(days=5),
        )
        self.o5 = OffCode.objects.create(
            price=10000,
            code='all',
            expire_date_time=timezone.now() + timedelta(days=5),
        )

    def test_d1(self):
        self.assertEqual(self.o1.code, 'off70')
        self.assertEqual(self.o1.percent, 70)
        self.assertEqual(self.o1.price, 0)
        self.assertEqual(self.o1.max, 150000)
        self.assertIsNone(self.o1.delete_time_stamp)
        self.assertFalse(self.o1.is_deleted)
        print(self.o1.is_deleted)
        self.assertFalse(self.o1.is_expired())
        print(self.o1.is_expired())

    def test_o2(self):
        self.assertEqual(self.o2.code, 'tabestan400')
        self.assertEqual(self.o2.percent, 0)
        self.assertEqual(self.o2.price, 30000)
        self.assertEqual(self.o2.max, 150000)

    def test_delete_discount(self):
        self.o1.my_delete()
        self.assertIsNotNone(self.o1.delete_time_stamp)
        self.assertTrue(self.o1.is_deleted)
        self.assertTrue(self.o1.is_expired())

    def test_final_price_percent(self):
        self.assertEqual(self.o1.final_price(100), 30)

    def test_final_price_percent_big(self):
        self.assertEqual(self.o1.final_price(1000000), 850000)

    def test_final_price_price(self):
        self.assertEqual(self.o2.final_price(40000), 10000)

    def test_final_price_price_big(self):
        self.assertRaises(AssertionError, self.o2.final_price, 29000)

    def test_o4(self):
        self.assertEqual(self.o4.percent, 0)
        self.assertEqual(self.o4.price, 10500)
        self.assertTrue(self.o4.is_expired())

    def test_o3(self):
        self.assertEqual(self.o3.percent, 22.5)
        self.assertEqual(self.o3.price, 0)
        self.assertEqual(self.o3.final_price(100), 78)
        print(self.o3.final_price(100))

    def test_o5(self):
        self.assertEqual(self.o5.code, 'all')
        self.assertEqual(self.o5.percent, 0)
        self.assertEqual(self.o5.price, 10000)
        self.assertEqual(self.o5.max, None)
        self.assertEqual(self.o5.final_price(11000), 1000)
        self.assertRaises(AssertionError, self.o5.final_price, 900)


"""
    Validators test
"""


class OffCodeValidatorTest(TestCase):
    def test1(self):
        self.assertRaises(ValidationError, off_code_validator, 'fg')

    def test2(self):
        self.assertRaises(ValidationError, off_code_validator, 'asfgg,gfd')

    def test3(self):
        self.assertRaises(ValidationError, off_code_validator, 'fg_jnlsdlkjg')

    def test4(self):
        self.assertRaises(ValidationError, off_code_validator, 'fgdhjfkjsdgfkhsdfkjhghdjdhhfhfdjsksdjhg')

    def test5(self):
        self.assertRaises(ValidationError, off_code_validator, 'salam_123')


class MenuItemNameValidatorTest(TestCase):
    def test1(self):
        self.assertRaises(ValidationError, menu_item_name_validator, 'f_g')

    def test2(self):
        self.assertRaises(ValidationError, menu_item_name_validator, 'asfgg,gfd')

    def test3(self):
        self.assertRaises(ValidationError, menu_item_name_validator, 'fg_jnlsdlkjg')

    def test4(self):
        self.assertRaises(ValidationError, menu_item_name_validator, 'fgdhjfkjsdgfkhsdfkjhghdjdhhfhfdjsksdjhg')

    def test5(self):
        self.assertRaises(ValidationError, menu_item_name_validator, 'salam123')


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


"""
    menu items models test
"""


class BrandTest(TestCase):
    def setUp(self) -> None:
        self.b1 = Brand.objects.create(
            name='Huawei',
        )

    def test_b1(self):
        self.assertEqual(self.b1.name, 'Huawei')

    def test_b1_menu_item_set(self):
        print(bool(self.b1.menuitem_set.all()))
        self.assertFalse(self.b1.menuitem_set.all())


class SpecificationTest(TestCase):
    def setUp(self) -> None:
        self.s1 = Specification.objects.create(
            name='color',
            value='red',
        )
        self.s2 = Specification.objects.create(
            name='ram',
            value='5',
        )
        self.s3 = VariableSpecification.objects.create(
            name='size',
            value='XXL',
        )

    def test_s1(self):
        self.assertEqual(self.s1.name, 'color')
        self.assertEqual(self.s1.value, 'red')

    def test_s2_menu_item_set(self):
        self.assertFalse(self.s1.menu_items.all())
        print("self.s1.menuitem_set : ", self.s1.menu_items.all())

    def test_s3_menu_item_set(self):
        self.assertEqual(self.s3.name, 'size')
        self.assertEqual(self.s3.value, 'XXL')
        self.assertFalse(self.s3.menu_item_variants.all())
        print("self.s3.menuitemvariant_set : ", self.s3.menu_item_variants.all())


class MenuItemTest(TestCase):
    def setUp(self) -> None:
        self.b1 = Brand.objects.create(
            name='Huawei',
        )
        self.s1 = Specification.objects.create(
            name='ram',
            value='6',
        )
        self.c1 = Category.objects.create(
            name='c1',
        )

        self.m1 = MenuItem.objects.create(
            name='m1',
            category=self.c1,
            brand=self.b1,
            description='m1 description',

        )

    def test_m1(self):
        self.m1.specifications.add(self.s1)
        self.assertIn(self.s1, self.m1.specifications.all())
        self.assertEqual(self.m1.category, self.c1)
        self.assertEqual(self.m1.name, 'm1')
        self.assertEqual(self.m1.brand, self.b1)
        self.assertEqual(self.m1.description, 'm1 description')
        self.assertFalse(self.m1.menuitemvariant_set.all())
        self.assertFalse(self.m1.image_set.all())


class MenuItemVariantTest(TestCase):
    def setUp(self) -> None:
        self.b1 = Brand.objects.create(
            name='Huawei',
        )
        self.ram = Specification.objects.create(
            name='ram',
            value='6',
        )
        self.color = VariableSpecification.objects.create(
            name='color',
            value='red',
        )
        self.size = VariableSpecification.objects.create(
            name='size',
            value='XXL',
        )
        self.c1 = Category.objects.create(
            name='c1',
        )

        self.m1 = MenuItem.objects.create(
            name='m1',
            category=self.c1,
            brand=self.b1,
            description='m1 description',

        )
        self.d1 = Discount.objects.create(
            is_percent=True,
            percent=70,
            max=150000,
            expire_date_time=timezone.now() + timedelta(days=5),
        )
        self.d2 = Discount.objects.create(
            is_percent=True,
            percent=70,
            max=150000,
            expire_date_time=timezone.now() - timedelta(days=5),
        )
        self.mv = MenuItemVariant.objects.create(
            menu_item=self.m1,
            price=1000000,
            count=50,
            discount=self.d1,
        )
        self.mv2 = MenuItemVariant.objects.create(
            menu_item=self.m1,
            price=1000000,
            count=50,
            discount=self.d2,
        )

    def test_mv2(self):
        self.mv2.variable_specifications.add(self.color)
        self.mv2.variable_specifications.add(self.size)
        self.assertEqual(self.mv2.menu_item, self.m1)
        self.assertEqual(self.mv2.menu_item.category, self.c1)
        self.assertEqual(self.mv2.final_price(), 1000000)
        self.mv2.discount = self.d1
        self.mv2.save()
        self.assertEqual(self.mv2.final_price(), 850000)
        print(self.mv2.variable_specifications.all())
        self.assertIn(self.color, self.mv2.variable_specifications.all())
        self.assertFalse(self.mv2.menu_item.image_set.all())

    def test_mv(self):
        self.mv.variable_specifications.add(self.color)
        self.mv.variable_specifications.add(self.size)
        self.assertEqual(self.mv.menu_item, self.m1)
        self.assertEqual(self.mv.menu_item.category, self.c1)
        self.assertEqual(self.mv.final_price(), 850000)
        print(self.mv.variable_specifications.all())
        self.assertIn(self.color, self.mv.variable_specifications.all())
        self.assertFalse(self.mv.menu_item.image_set.all())

    def test_m1(self):
        print(self.m1.menuitemvariant_set.all())
        self.assertIn(self.mv, self.m1.menuitemvariant_set.all())
