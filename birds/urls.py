from django.urls import path

from .views import BirdsView, SingleBirdsView, VersionView

app_name = "birds"

urlpatterns = [
    path('birds', BirdsView.as_view()),
    path('birds/<slug:name>', SingleBirdsView.as_view()),
    path('version', VersionView.as_view()),
]
