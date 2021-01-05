from djservices import BaseService, CommonCRUDService, UserCRUDService

from .models import (
    TestModel, TestModelWithUserField, TestModelWithAuthorField
)
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


class TestCommonCRUDService(CommonCRUDService):
    model = TestModel


class TestUserCRUDService(UserCRUDService):
    model = TestModelWithUserField


class TestUserCRUDServiceWithUserFieldName(UserCRUDService):
    model = TestModelWithAuthorField
    user_field_name = 'author'
