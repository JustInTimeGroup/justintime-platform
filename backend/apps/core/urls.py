from django.urls import path

from .views import AboutView, ContactView, ContactThanksView, HomeView, PortalHomeView, ServicesView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("services/", ServicesView.as_view(), name="services"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("contact/thanks/", ContactThanksView.as_view(), name="contact_thanks"),
    path("portal/", PortalHomeView.as_view(), name="portal_home"),
]
