from django.test import TestCase

from djservices.base import BaseService, BaseCRUDService, CRUDService
from djservices.strategies import BaseCRUDStrategy

from testapp.models import TestModel
from testapp.forms import TestForm


class ServiceWithoutModel(BaseService):
    pass


class CRUDServiceWithoutStrategyClass(BaseCRUDService):
    model = TestModel


class CRUDServiceWithoutForm(CRUDService):
    model = TestModel


class CRUDStrategy(BaseCRUDStrategy):
    pass


class ServicesExceptionsTests(TestCase):

    def test_without_model_attribute(self):
        with self.assertRaises(AttributeError,
                msg="You need to set `model` attribute"):
            ServiceWithoutModel()

    def test_base_crud_service_without_strategy_class_attribute(self):
        with self.assertRaises(AttributeError,
                msg="You need to set `strategy_class` attribute"):
            CRUDServiceWithoutStrategyClass()

    def test_crud_service_without_form_attribute(self):
        with self.assertRaises(AttributeError,
                msg="You need to set `form` attribute"):
            CRUDServiceWithoutForm()


class BaseCRUDStrategyExceptionsTests(TestCase):

    def setUp(self):
        self.strategy = CRUDStrategy(TestModel)

    def test_get_all(self):
        with self.assertRaises(NotImplementedError):
            self.strategy.get_all()

    def test_get_concrete(self):
        with self.assertRaises(NotImplementedError):
            self.strategy.get_concrete(1)

    def test_create(self):
        with self.assertRaises(NotImplementedError):
            self.strategy.create({'test': 'data'})

    def test_change(self):
        with self.assertRaises(NotImplementedError):
            self.strategy.change({'test': 'data'}, 1)

    def test_delete(self):
        with self.assertRaises(NotImplementedError):
            self.strategy.delete(1)
