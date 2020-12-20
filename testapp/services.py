from djservices import BaseService, CRUDService

from .models import TestModel, TestModelWithUserField
from .forms import TestForm, TestModelForm


class Empty:

    def __init__(self, *args, **kwargs):
        pass


class SimpleService(BaseService):
    strategy_class = Empty
    model = Empty

    def get_one(self):
        return 1


class SimpleServiceWithoutStrategy(BaseService):
    model = Empty

    def get_one(self):
        return 1


class TestCRUDService(CRUDService):
    model = TestModel
    form = TestForm


class TestCRUDServiceWithChangeForm(CRUDService):
    model = TestModel
    form = TestForm
    change_form = TestForm


class TestCRUDServiceWithChangeModelForm(CRUDService):
    model = TestModel
    form = TestForm
    change_form = TestModelForm


class TestCRUDServiceWithExtendedParameters(CRUDService):
    model = TestModelWithUserField
    form = TestForm
