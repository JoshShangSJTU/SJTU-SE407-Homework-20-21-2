from django.urls import path
from mgr import sign_in_out
from mgr import team
from mgr import player
from mgr import match

urlpatterns = [

    path('signin', sign_in_out.signin),
    path('signout', sign_in_out.signout),
    path('team', team.dispatcher),
    path('player', player.dispatcher),
    path('match', match.dispatcher),

]
