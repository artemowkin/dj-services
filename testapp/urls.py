from django.urls import path

from . import views


urlpatterns = [
    path('list/', views.TestListView.as_view(), name='list_view'),
    path(
        'detail/<int:pk>/', views.TestDetailView.as_view(),
        name='detail_view'
    ),
]
