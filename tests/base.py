import os

from django.db.models import Model
from django.test import TestCase
from django.forms import Form, ModelForm
from django.contrib.auth import get_user_model

from djservices import BaseService, CommonCRUDService, UserCRUDService

from testapp.models import (
    TestModel, TestModelWithUserField, TestModelWithAuthorField
)
from testapp.forms import TestForm, TestModelForm
from testapp.services import (
    Empty, SimpleService, SimpleServiceWithoutStrategy,
    TestCommonCRUDService, TestUserCRUDService,
    TestUserCRUDServiceWithUserFieldName
)


User = get_user_model()


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


class TestCommonCRUDServiceTests(TestCase):

    def setUp(self):
        self.service = TestCommonCRUDService()
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
        entry = self.service.create(data)
        self.assertEqual(entry.title, data['title'])

    def test_change(self):
        data = {'title': 'new_title'}
        form = TestForm(data)
        self.assertTrue(form.is_valid())
        entry = self.service.change(self.entry, form)
        self.assertEqual(entry.title, data['title'])
        all_entries = self.service.get_all()
        self.assertEqual(len(all_entries), 1)
        self.assertEqual(all_entries[0], entry)

    def test_change_with_model_form(self):
        data = {'title': 'new_title'}
        form = TestModelForm(data, instance=self.entry)
        self.assertTrue(form.is_valid())
        entry = self.service.change(self.entry, form)
        self.assertEqual(entry.title, data['title'])
        all_entries = self.service.get_all()
        self.assertEqual(len(all_entries), 1)
        self.assertEqual(all_entries[0], entry)

    def test_delete(self):
        self.service.delete(self.entry)
        all_entries = self.service.get_all()
        self.assertEqual(len(all_entries), 0)


class TestUserCRUDServiceTests(TestCase):

    def setUp(self):
        self.service = TestUserCRUDService()
        self.user = User.objects.create_superuser(
            username='testuser', password='testpass'
        )
        self.entry = TestModelWithUserField.objects.create(
            title='test', user=self.user
        )

    def test_get_all(self):
        all_entries = self.service.get_all(self.user)
        self.assertEqual(len(all_entries), 1)
        self.assertEqual(all_entries[0], self.entry)

    def test_get_concrete(self):
        entry = self.service.get_concrete(self.entry.pk, self.user)
        self.assertEqual(entry, self.entry)

    def test_create(self):
        data = {'title': 'new_entry'}
        entry = self.service.create(data, self.user)
        self.assertEqual(entry.title, data['title'])
        self.assertEqual(entry.user, self.user)

    def test_change(self):
        data = {'title': 'new_title'}
        form = TestForm(data)
        self.assertTrue(form.is_valid())
        entry = self.service.change(self.entry, form)
        self.assertEqual(entry.title, data['title'])
        self.assertEqual(entry.user, self.user)
        all_entries = self.service.get_all(self.user)
        self.assertEqual(len(all_entries), 1)
        self.assertEqual(all_entries[0], entry)

    def test_change_with_model_form(self):
        data = {'title': 'new_title'}
        form = TestModelForm(data, instance=self.entry)
        self.assertTrue(form.is_valid())
        entry = self.service.change(self.entry, form)
        self.assertEqual(entry.title, data['title'])
        self.assertEqual(entry.user, self.user)
        all_entries = self.service.get_all(self.user)
        self.assertEqual(len(all_entries), 1)
        self.assertEqual(all_entries[0], entry)

    def test_delete(self):
        self.service.delete(self.entry)
        all_entries = self.service.get_all(self.user)
        self.assertEqual(len(all_entries), 0)


class TestUserCRUDServiceWithUserFieldNameTests(TestCase):

    def setUp(self):
        self.service = TestUserCRUDServiceWithUserFieldName()
        self.user = User.objects.create_superuser(
            username='testuser', password='testpass'
        )
        self.entry = TestModelWithAuthorField.objects.create(
            title='test', author=self.user
        )

    def test_get_all(self):
        all_entries = self.service.get_all(self.user)
        self.assertEqual(len(all_entries), 1)
        self.assertEqual(all_entries[0], self.entry)

    def test_get_concrete(self):
        entry = self.service.get_concrete(self.entry.pk, self.user)
        self.assertEqual(entry, self.entry)

    def test_create(self):
        data = {'title': 'new_entry'}
        entry = self.service.create(data, self.user)
        self.assertEqual(entry.title, data['title'])
        self.assertEqual(entry.author, self.user)

    def test_change(self):
        data = {'title': 'new_title'}
        form = TestForm(data)
        self.assertTrue(form.is_valid())
        entry = self.service.change(self.entry, form)
        self.assertEqual(entry.title, data['title'])
        self.assertEqual(entry.author, self.user)
        all_entries = self.service.get_all(self.user)
        self.assertEqual(len(all_entries), 1)
        self.assertEqual(all_entries[0], entry)

    def test_change_with_model_form(self):
        data = {'title': 'new_title'}
        form = TestModelForm(data, instance=self.entry)
        self.assertTrue(form.is_valid())
        entry = self.service.change(self.entry, form)
        self.assertEqual(entry.title, data['title'])
        self.assertEqual(entry.author, self.user)
        all_entries = self.service.get_all(self.user)
        self.assertEqual(len(all_entries), 1)
        self.assertEqual(all_entries[0], entry)

    def test_delete(self):
        self.service.delete(self.entry)
        all_entries = self.service.get_all(self.user)
        self.assertEqual(len(all_entries), 0)
