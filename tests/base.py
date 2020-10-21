import os

from django.db.models import Model
from django.test import TestCase
from django.forms import Form

from djservices import BaseService, CRUDService

from testapp.models import TestModel
from testapp.forms import TestForm


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


class BaseServiceTests(TestCase):

    def setUp(self):
        self.service = SimpleService()
        self.service_without_strategy = SimpleServiceWithoutStrategy()

    def test_get_one(self):
        self.assertEqual(self.service.get_one(), 1)
        self.assertEqual(self.service_without_strategy.get_one(), 1)

    def test_configuration(self):
        self.assertTrue(hasattr(self.service, 'model'))
        self.assertTrue(hasattr(self.service_without_strategy, 'model'))
        self.assertTrue(hasattr(self.service, 'strategy_class'))
        self.assertIsNone(self.service_without_strategy.strategy_class)
        self.assertEqual(self.service.model, Empty)
        self.assertEqual(self.service_without_strategy.model, Empty)
        self.assertEqual(self.service.strategy_class, Empty)


class TestCRUDServiceTests(TestCase):

    def setUp(self):
        self.service = TestCRUDService()
        self.entry = TestModel.objects.create(title='test')

    def test_get_all(self):
        all_entries = self.service.get_all()
        self.assertEqual(len(all_entries), 1)
        self.assertEqual(all_entries[0], self.entry)

    def test_get_concrete(self):
        entry = self.service.get_concrete(self.entry.pk)
        self.assertEqual(entry, self.entry)

    def test_create(self):
        data = {'title': 'new_entry'}
        bad_data = {'field': 'value'}
        response = self.service.create(data)
        bad_response = self.service.create(bad_data)
        self.assertIsInstance(response, Model)
        self.assertIsInstance(bad_response, Form)
        self.assertEqual(response.title, data['title'])

    def test_change(self):
        data = {'title': 'new_title'}
        bad_data = {'field': 'value'}
        response = self.service.change(data, self.entry.pk)
        self.assertIsInstance(response, Model)
        self.assertEqual(response.title, data['title'])
        bad_response = self.service.change(bad_data, self.entry.pk)
        self.assertIsInstance(bad_response, Form)

    def test_delete(self):
        self.service.delete(self.entry.pk)
        all_entries = self.service.get_all()
        self.assertEqual(len(all_entries), 0)

    def test_get_create_form(self):
        form = self.service.get_create_form()
        self.assertIsInstance(form, Form)

    def test_get_change_form(self):
        form = self.service.get_change_form(self.entry.pk)
        self.assertIsInstance(form, Form)
        self.assertTrue(form.is_valid())
