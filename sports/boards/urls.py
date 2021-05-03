from django.conf.urls import url, include
from django.urls import path

from .views import *


urlpatterns = [
    path('add_book/', add_book, ),
    path('show_books/', show_books, ),
]