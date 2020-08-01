from django.urls import path

from .views import BirdsView, SingleBirdsView

app_name = "birds"

urlpatterns = [
    path('birds/', BirdsView.as_view()),
    path('birds/<slug:name>', SingleBirdsView.as_view()),
]