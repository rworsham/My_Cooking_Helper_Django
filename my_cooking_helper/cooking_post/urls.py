from django.urls import path
from . import views

app_name = "cooking_post"
urlpatterns = [
    path('', views.landing_page, name="landing_page"),
    path("login", views.login_page, name="login_page"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("recipes", views.recipes, name="recipes"),
    path("featured recipes", views.featured_recipes, name="featured_recipes"),
    path("sign_up", views.sign_up, name="sign_up")
]