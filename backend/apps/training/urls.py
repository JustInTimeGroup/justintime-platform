from django.urls import path

from .views import TrainingApplyView, TrainingDetailView, TrainingListView, TrainingThanksView

app_name = "training"

urlpatterns = [
    path("", TrainingListView.as_view(), name="list"),
    path("thanks/", TrainingThanksView.as_view(), name="thanks"),
    path("<slug:slug>/", TrainingDetailView.as_view(), name="detail"),
    path("<slug:slug>/register/", TrainingApplyView.as_view(), name="register"),
]