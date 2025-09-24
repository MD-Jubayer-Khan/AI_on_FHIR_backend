from django.urls import path
from .views import QueryView, Suggestions

urlpatterns = [
    path('query/', QueryView.as_view(), name='query'),
    path('suggestions/', Suggestions, name='suggestions'), 
]