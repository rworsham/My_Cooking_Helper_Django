from django.urls import path
from . import views

app_name = "cooking_post"
urlpatterns = [
    path('', views.landing_page, name="landing"),
    path("login", views.login_page, name="login_page"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("recipes", views.recipes, name="recipes")
]