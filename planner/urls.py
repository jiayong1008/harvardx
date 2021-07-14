from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("trip/", views.trip, name="trip"),
    path("trip/<int:trip_id>/", views.detailTrip, name="detail-trip"),
    path("trip/<int:trip_id>/recommendations/", views.recommendation, name="recommendation")
]