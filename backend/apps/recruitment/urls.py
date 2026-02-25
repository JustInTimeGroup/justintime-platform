from django.urls import path

from .views import (
    CareerThanksView,
    JobApplyView,
    JobDetailView,
    JobListView,
)

app_name = "recruitment"

urlpatterns = [
    path("", JobListView.as_view(), name="list"),
    path("thanks/", CareerThanksView.as_view(), name="thanks"),
    path("<slug:slug>/", JobDetailView.as_view(), name="detail"),
    path("<slug:slug>/apply/", JobApplyView.as_view(), name="apply"),
]