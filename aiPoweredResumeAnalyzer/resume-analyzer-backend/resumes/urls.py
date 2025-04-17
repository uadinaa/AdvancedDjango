from django.urls import path
from .views import ResumeUploadView, ResumeParsedView
from . import views


urlpatterns = [
    path('upload/', ResumeUploadView.as_view(), name='resume-upload'),
    path('parsed-resume/', ResumeParsedView.as_view(), name='parsed-resume'),
    path('', views.ResumeListView.as_view(), name='resume-list'),
    path('<str:pk>/', views.ResumeDetailView.as_view(), name='resume-detail'),
    path('<str:pk>/delete/', views.ResumeDeleteView.as_view(), name='resume-delete'),
]
