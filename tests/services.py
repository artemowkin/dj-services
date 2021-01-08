import os

from django.db.models import Model
from django.test import TestCase
from django.forms import Form, ModelForm
from django.contrib.auth import get_user_model
from django.http import Http404

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

    def test_service_get_one(self):
        service_result = self.service.get_one()
        self.assertEqual(service_result, 1)

    def test_service_without_strategy_get_one(self):
        without_strategy_result = self.service_without_strategy.get_one()
        self.assertEqual(without_strategy_result, 1)


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

    def test_change_with_model_form(self):
        data = {'title': 'new_title'}
        form = TestModelForm(data, instance=self.entry)

        self.assertTrue(form.is_valid())

        entry = self.service.change(self.entry, form)

        self.assertEqual(entry.title, data['title'])

    def test_delete(self):
        all_entries_before_deleting = self.service.get_all()
        self.assertEqual(len(all_entries_before_deleting), 1)

        self.service.delete(self.entry)
        all_entries_after_deleting = self.service.get_all()

        self.assertEqual(len(all_entries_after_deleting), 0)


class UserServiceTests(TestCase):

    def setUp(self):
        self.service = None
        self.user_field_name = None
        self.user = User.objects.create_superuser(
            username='testuser', password='testpass'
        )
        self.bad_user = User.objects.create_superuser(
            username='testuser2', password='testpass'
        )
        self.entry = TestModelWithUserField.objects.create(
            title='test', user=self.user
        )

    def test_get_all_user(self):
        all_user_entries = self.service.get_all(self.user)

        self.assertEqual(len(all_user_entries), 1)
        self.assertEqual(all_user_entries[0], self.entry)

    def test_get_all_bad_user(self):
        all_bad_user_entries = self.service.get_all(self.bad_user)

        self.assertEqual(len(all_bad_user_entries), 0)
        self.assertNotIn(self.entry, all_bad_user_entries)

    def test_get_concrete_user(self):
        entry = self.service.get_concrete(self.entry.pk, self.user)

        self.assertEqual(entry, self.entry)

    def test_get_concrete_bad_user(self):
        with self.assertRaises(Http404):
            self.service.get_concrete(self.entry.pk, self.bad_user)

    def test_create(self):
        data = {'title': 'new_entry'}
        entry = self.service.create(data, self.user)
        entry_user_field = getattr(entry, self.user_field_name)

        self.assertEqual(entry.title, data['title'])
        self.assertEqual(entry_user_field, self.user)

    def test_change(self):
        data = {'title': 'new_title'}
        form = TestForm(data)

        self.assertTrue(form.is_valid())

        entry = self.service.change(self.entry, form)

        self.assertEqual(entry.title, data['title'])

    def test_change_with_model_form(self):
        data = {'title': 'new_title'}
        form = TestModelForm(data, instance=self.entry)

        self.assertTrue(form.is_valid())

        entry = self.service.change(self.entry, form)

        self.assertEqual(entry.title, data['title'])

    def test_delete(self):
        self.service.delete(self.entry)
        all_entries_after_deleting = self.service.get_all(self.user)

        self.assertEqual(len(all_entries_after_deleting), 0)


class TestUserCRUDServiceTests(UserServiceTests):

    def setUp(self):
        super().setUp()
        self.service = TestUserCRUDService()
        self.user_field_name = 'user'


class TestUserCRUDServiceWithUserFieldNameTests(UserServiceTests):

    def setUp(self):
        super().setUp()
        self.service = TestUserCRUDServiceWithUserFieldName()
        self.user_field_name = 'author'
        self.entry = TestModelWithAuthorField.objects.create(
            title='test', author=self.user
        )
