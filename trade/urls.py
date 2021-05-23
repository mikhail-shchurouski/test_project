from django.urls import path, include
from .views import *

urlpatterns = [
    path('', HomeContract.as_view(), name='home'),
    path('search/', get_id, name='search'),

]