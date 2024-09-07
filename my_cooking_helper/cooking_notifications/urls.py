from django.urls import path
from . import views

app_name = "cooking_notifications"
urlpatterns = [
    path("contact", views.contact, name="contact"),
]