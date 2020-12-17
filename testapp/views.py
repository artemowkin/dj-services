from djservices.views import ListView, DetailView

from .services import TestCRUDService


class TestListView(ListView):
    service = TestCRUDService()
    template_name = 'test_list_view.html'


class TestDetailView(DetailView):
    service = TestCRUDService()
    template_name = 'test_detail_view.html'
