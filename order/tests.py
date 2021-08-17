from datetime import timedelta

from django.test import TestCase
from .models import *
from customer.models import *
from product.models import *


# Create your tests here.

class OrderTest(TestCase):
    def setUp(self) -> None:
        self.u1 = User.objects.create_user(
            phone='+989117898739',
            email='amir.talebi@gmail.com',
        )
        self.u1.set_password('1234')
        self.c1 = Customer.objects.create(
            user=self.u1,
        )
        self.off1 = OffCode.objects.create(
            is_percent=True,
            percent=70,
            max=150000,
            code='off70',
            expire_date_time=timezone.now() + timedelta(days=5),
        )
        self.o1 = Order.objects.create(
            customer=self.c1,
            off_code=self.off1,
            status='d',  # during , paid , canceled
        )
        self.o2 = Order.objects.create(
            customer=self.c1,
        )
        self.o3 = Order.objects.create(
            customer=self.c1,
            status='p',  # during , paid , canceled
        )
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
        self.cat1 = Category.objects.create(
            name='c1',
        )

        self.m1 = MenuItem.objects.create(
            name='m1',
            category=self.cat1,
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
        self.o_m = OrderMenuItem.objects.create(
            order=self.o1,
            menu_item_variant=self.mv,
            quantity=10,
        )

    def test1(self):
        self.assertEqual(self.o1.off_code, self.off1)

    def test2(self):
        self.assertEqual(self.o1.customer, self.c1)
        self.assertEqual(self.o2.customer, self.c1)
        self.assertEqual(self.o3.customer, self.c1)

    def test3(self):
        self.o2.off_code = self.off1
        self.o2.save()

    def test4(self):
        self.assertEqual(self.o1.final_price(), 8350000)

    def test5(self):
        self.assertEqual(self.o1.pure_price(), 8500000)

    def test6(self):
        self.o1.off_code = None
        self.o1.save()
        self.assertEqual(self.o1.final_price(), 8500000)

    def test7(self):
        print(self.o1.status)
        self.assertEqual(self.o1.status, 'd')
        self.assertEqual(self.o2.status, 'd')
        self.assertEqual(self.o3.status, 'p')
