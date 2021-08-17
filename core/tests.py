from django.test import TestCase

# Create your tests here.
from .models import TestModel, User
from .validators import *
from .utils import *

"""
BaseModel Test
"""


class TestModelTest(TestCase):
    def setUp(self) -> None:
        self.test_model1 = TestModel.objects.create(
            is_deleted=False,
        )
        self.test_model2 = TestModel.objects.create(
            is_deleted=True,
        )
        self.test_model3 = TestModel.objects.create(
            is_deleted=True,
        )
        self.test_model4 = TestModel.objects.create()

    def test_is_deleted_test_model1(self):
        self.assertFalse(self.test_model1.is_deleted)

    def test_is_deleted_test_model2(self):
        self.assertTrue(self.test_model2.is_deleted)

    def test_delete_test_model1(self):
        self.test_model1.my_delete()
        self.assertTrue(self.test_model1.is_deleted)

    def test_delete_test_model2(self):
        self.test_model2.my_delete()
        self.assertTrue(self.test_model2.is_deleted)

    def test_delete_time_stamp_None_test_model1(self):
        self.assertIsNone(self.test_model1.delete_time_stamp)

    def test_delete_time_stamp_None_test_model4(self):
        self.assertIsNone(self.test_model1.delete_time_stamp)

    def test_delete_time_stamp_not_None_test_model1(self):
        self.test_model1.my_delete()
        self.assertIsNotNone(self.test_model1.delete_time_stamp)

    def test_delete_time_stamp_not_None_test_model4(self):
        self.test_model4.my_delete()
        self.assertIsNotNone(self.test_model4.delete_time_stamp)

    def test_create_time_stamp_is_not_None_test_model1(self):
        self.assertIsNotNone(self.test_model1.create_time_stamp)

    def test_modify_time_stamp_is_not_None_test_model1(self):
        self.assertIsNotNone(self.test_model1.modify_time_stamp)

    def test_modify_equal_create_test_model1(self):
        self.assertEqual(self.test_model1.create_time_stamp, self.test_model1.modify_time_stamp)

    def test_modify_not_equal_create_test_model1(self):
        self.test_model1.my_delete()
        self.assertNotEqual(self.test_model1.create_time_stamp, self.test_model1.modify_time_stamp)

    def test_objects_all(self):
        self.assertNotIn(self.test_model2, TestModel.objects.all())

    def test_objects_all2(self):
        self.test_model1.my_delete()
        print(self.test_model1.delete_time_stamp)
        print(self.test_model1.create_time_stamp)
        print(self.test_model1.modify_time_stamp)
        print(self.test_model1.is_deleted)
        self.assertNotIn(self.test_model1, TestModel.objects.all())

    def test_objects_all3(self):
        self.assertIn(self.test_model1, TestModel.objects.all())

    def test_objects_filter(self):
        print(self.test_model2.delete_time_stamp)
        print(self.test_model2.create_time_stamp)
        print(self.test_model2.modify_time_stamp)
        print(self.test_model2.is_deleted)
        self.assertIn(self.test_model1, TestModel.objects.filter())

    def test_objects_filter2(self):
        self.test_model1.delete()
        self.assertNotIn(self.test_model1, TestModel.objects.filter())

    def test_objects_filter3(self):
        self.assertNotIn(self.test_model2, TestModel.objects.filter())

    def test_archive(self):
        self.assertIn(self.test_model2, TestModel.objects.archive())

    def test_archive1(self):
        self.assertIn(self.test_model1, TestModel.objects.archive())

    def test_archive2(self):
        self.test_model1.delete()
        self.assertNotIn(self.test_model1, TestModel.objects.archive())


'''
Test Validators
'''


class PhoneValidatorTest(TestCase):
    def test1(self):
        self.assertRaises(ValidationError, phone_validator, '346456')

    def test2(self):
        self.assertRaises(ValidationError, phone_validator, '0911789')

    def test3(self):
        self.assertRaises(ValidationError, phone_validator, '+98911789')

    def test4(self):
        self.assertRaises(ValidationError, phone_validator, '0911789873999')

    def test5(self):
        self.assertRaises(ValidationError, phone_validator, '+98911789873999')

    def test6(self):
        self.assertRaises(ValidationError, phone_validator, '0911789873_')

    def test7(self):
        self.assertRaises(ValidationError, phone_validator, '09117898739')


"""
Core.User Test
"""


class UserTest(TestCase):
    def setUp(self) -> None:
        self.u1 = User.objects.create(
            phone='+989117898739',
        )

    def test1(self):
        self.assertEqual(self.u1.phone, '+989117898739')

    def test2(self):
        self.u1.is_staff = False
        self.assertFalse(self.u1.is_staff)

    def test3(self):
        self.u1.set_password('1234')
        self.u1.save()
        self.assertTrue(self.u1.check_password('1234'))

    def test4(self):
        self.u1.first_name = 'amir'
        self.assertEqual(self.u1.first_name, 'amir')

    def test5(self):
        self.u1.last_name = 'talebi'
        self.assertEqual(self.u1.last_name, 'talebi')
