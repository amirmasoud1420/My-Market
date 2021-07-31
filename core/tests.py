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

    def test_is_deleted_test_model1(self):
        self.assertFalse(self.test_model1.is_deleted)

    def test_is_deleted_test_model2(self):
        self.assertTrue(self.test_model2.is_deleted)

    def test_delete_test_model1(self):
        self.test_model1.delete()
        self.assertTrue(self.test_model1.is_deleted)

    def test_delete_test_model2(self):
        self.test_model2.delete()
        self.assertTrue(self.test_model2.is_deleted)

