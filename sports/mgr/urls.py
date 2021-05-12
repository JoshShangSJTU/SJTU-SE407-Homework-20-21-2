from django.urls import path
from mgr import sign_in_out
from mgr import team

urlpatterns = [

    path('signin', sign_in_out.signin),
    path('signout', sign_in_out.signout),
    path('team', team.dispatcher),

]
