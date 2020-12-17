from __future__ import annotations

from typing import Any

from django.views import View
from django.core.exceptions import ImproperlyConfigured
from django.db.models import QuerySet, Model
from django.shortcuts import render


class BaseGenericServiceView(View):
    """Base class for all generic views

    Attributes
    ----------
    service : Service
        Service used in generic views
    template_name : str
        Name of renderred template
    context_object_name : str
        Name of context object

    Methods
    -------
    get(request, *args, **kwargs)
        Renders template

    """

    service = None
    template_name = ''
    context_object_name = ''

    def __init__(self, *args, **kwargs):
        if not self.service:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} is missing a service attribute"
            )

        if not self.template_name:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} is missing a "
                "template_name attribute"
            )

        if not self.context_object_name:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} is missing a "
                "context_object_name attribute"
            )

        super().__init__(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        """Renders `template_name` with context from `get_context` method"""
        context_data = self.get_context(*args, **kwargs)
        return render(request, self.template_name, context_data)


class ListView(BaseGenericServiceView):
    """Generic view that displays list of model entries

    Attributes
    ----------
    context_object_name : str
        Name of context object. By default it's `object_list`

    Methods
    -------
    get_queryset()
        Returns QuerySet with list of entries
    get_context()
        Returns context data

    """

    context_object_name = 'object_list'

    def get_queryset(self) -> QuerySet:
        """Returns all model entries"""
        return self.service.get_all()

    def get_context(self) -> dict:
        """
        Returns context dict with all model entries from `get_queryset`
        method
        """
        self.object_list = self.get_queryset()
        return {self.context_object_name: self.object_list}


class DetailView(BaseGenericServiceView):
    """Generic view that displays the single model entry

    Attributes
    ----------
    context_object_name : str
        Name of context object. By default it's `object`

    Methods
    -------
    get_object(pk)
        Returns model entry
    get_context(pk)
        Returns context data

    """

    context_object_name = 'object'

    def get_object(self, pk: Any) -> Model:
        """Returns a concrete entry with `pk`"""
        return self.service.get_concrete(pk)

    def get_context(self, pk: Any) -> dict:
        """
        Returns context dict with the concrete model entry from
        `get_object` method
        """
        self.instance = self.get_object(pk)
        return {self.context_object_name: self.instance}
