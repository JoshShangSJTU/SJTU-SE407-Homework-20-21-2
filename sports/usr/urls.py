from django.urls import path
from usr import sign_in_out
from usr import reg

urlpatterns = [

    path('signin', sign_in_out.signin),
    path('signout', sign_in_out.signout),
    path('register',reg.register)
]