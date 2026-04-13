from django.urls import path
from .views import get_highlights

urlpatterns = [
    path('highlights/', get_highlights, name='highlights'),
]