from django.test import TestCase

# Create your tests here.
from .models import TestModel


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
