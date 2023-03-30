from .views import *
from django.urls import path

urlpatterns = [
    path("team-register/", view=TeamRegister.as_view(), name="team-register"),
    path("login/", view=Login.as_view(), name="login")
]
