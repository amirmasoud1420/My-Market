from django.test import TestCase

# Create your tests here.
from .models import *


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
