from django.test import TestCase

from djservices.base import BaseService, BaseCRUDService, CommonCRUDService

from testapp.models import TestModel
from testapp.forms import TestForm


class ServiceWithoutModel(BaseService):
    pass


class CRUDServiceWithoutStrategyClass(BaseCRUDService):
    model = TestModel


class CRUDServiceWithoutForm(CommonCRUDService):
    model = TestModel


class ServicesExceptionsTests(TestCase):

    def test_without_model_attribute(self):
        with self.assertRaises(AttributeError,
                msg="You need to set `model` attribute"):
            ServiceWithoutModel()

    def test_base_crud_service_without_strategy_class_attribute(self):
        with self.assertRaises(AttributeError,
                msg="You need to set `strategy_class` attribute"):
            CRUDServiceWithoutStrategyClass()
