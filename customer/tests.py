from django.test import TestCase
from .models import *


# Create your tests here.


class CustomerTest(TestCase):
    def setUp(self) -> None:
        self.u1 = User.objects.create_user(
            phone='+989117898739',
            email='amir.talebi@gmail.com',
        )
        self.u1.set_password('1234')
        self.c1 = Customer.objects.create(
            user=self.u1,
        )

    def test1(self):
        self.assertEqual(self.c1.user, self.u1)

    def test2(self):
        self.assertTrue(self.c1.user.check_password('1234'))

    def test3(self):
        print(self.c1.image)
        self.assertIsNotNone(self.c1.image)

    def test4(self):
        self.assertEqual(self.c1.user.phone, '+989117898739')

    def test5(self):
        self.assertEqual(self.c1.user.email, 'amir.talebi@gmail.com')

    def test6(self):
        self.assertEqual(self.c1.user.username, '+989117898739')


class AddressTest(TestCase):
    def setUp(self) -> None:
        self.u1 = User.objects.create_user(
            phone='+989117898739',
            email='amir.talebi@gmail.com',
        )
        self.u1.set_password('1234')
        self.c1 = Customer.objects.create(
            user=self.u1,
        )
        self.a1 = Address.objects.create(
            owner=self.c1,
            state='mazandaran',
            city='babol',
            postal_code='34656754',
            lat=39.56,
            lng=12.4557,
            detail='roshan36 pelak 1006 aghil talebnia',

        )

    def test1(self):
        self.assertEqual(self.a1.lat, 39.56)
        self.assertEqual(self.a1.lng, 12.4557)

    def test2(self):
        self.assertEqual(self.a1.owner, self.c1)
        self.assertEqual(self.a1.owner.user, self.u1)

    def test3(self):
        self.assertEqual(self.a1.state, 'mazandaran')
        self.assertEqual(self.a1.city, 'babol')
        self.assertEqual(self.a1.detail, 'roshan36 pelak 1006 aghil talebnia')
        self.assertEqual(self.a1.postal_code, '34656754')

    def test4(self):
        self.assertTrue(self.a1.owner.user.check_password('1234'))

    def test5(self):
        self.u1.set_password('12345')
        self.u1.save()
        self.assertTrue(self.a1.owner.user.check_password('12345'))
