from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ImproperlyConfigured

from djservices.views import BaseGenericServiceView
from testapp.models import TestModel


class BrokenViewWithoutService(BaseGenericServiceView):
    template_name = 'test_template'
    context_object_name = 'test_context_name'


class BrokenViewWithoutTemplateName(BaseGenericServiceView):
    service = 'test_service'
    context_object_name = 'test_context_name'


class BrokenViewWithoutContextObjectName(BaseGenericServiceView):
    service = 'test_service'
    template_name = 'test_template'


class BaseGenericServiceViewTests(TestCase):

    def test_view_attributes(self):
        with self.assertRaises(ImproperlyConfigured):
            BrokenViewWithoutService()

        with self.assertRaises(ImproperlyConfigured):
            BrokenViewWithoutTemplateName()

        with self.assertRaises(ImproperlyConfigured):
            BrokenViewWithoutContextObjectName()


class ListViewTests(TestCase):

    def setUp(self):
        self.entry = TestModel.objects.create(title='testtitle')

    def test_list_view(self):
        response = self.client.get(reverse('list_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'test_list_view.html')
        self.assertContains(response, self.entry.title)


class DetailViewTests(TestCase):

    def setUp(self):
        self.entry = TestModel.objects.create(title='testtitle')

    def test_list_view(self):
        response = self.client.get(
            reverse('detail_view', args=[self.entry.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'test_detail_view.html')
        self.assertContains(response, self.entry.title)
