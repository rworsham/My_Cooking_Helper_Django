from django.urls import path
from . import views

app_name = "cooking_post"
urlpatterns = [
    path("", views.login_page, name="login_page"),
]