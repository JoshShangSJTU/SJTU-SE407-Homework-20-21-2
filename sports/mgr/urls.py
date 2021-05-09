from django.urls import path
from mgr import sign_in_out
from mgr import sportsdata

urlpatterns = [

    path('signin', sign_in_out.signin),
    path('signout', sign_in_out.signout),
    path('sportdata', sportsdata.dispatcher),

]
