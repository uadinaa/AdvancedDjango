from django.urls import path
from .views import MatchJobsView

urlpatterns = [
    path('match/<int:user_id>/', MatchJobsView.as_view(), name='match-jobs'),
]
