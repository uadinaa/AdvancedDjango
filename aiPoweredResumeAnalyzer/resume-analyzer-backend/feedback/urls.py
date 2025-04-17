from django.urls import path
from .views import (
    ResumeFeedbackView, ResumeFeedbackFromMongoView, ResumeRatingView,
    ResumeRatingFromMongoView, test_rating_view, rating_form_view,
    my_rating_history, view_rating_history, export_ratings_csv,
    export_ratings_pdf)


urlpatterns = [
    path("feedback/", ResumeFeedbackView.as_view(), name="resume-feedback"),
    path("feedback/from-mongo/", ResumeFeedbackFromMongoView.as_view(), name="resume-feedback-from-mongo"),
    path("rate/", ResumeRatingView.as_view(), name="resume-rating"),
    path("rate/from-mongo/", ResumeRatingFromMongoView.as_view(), name="resume-rating-from-mongo"),
    path("rating-preview/", test_rating_view),
    path("rate-resume/", rating_form_view),
    path("view-rating/", view_rating_history),
    path("my-ratings/", my_rating_history, name="my_ratings"),
    path("my-ratings/export/csv/", export_ratings_csv, name="export_ratings_csv"),
    path("my-ratings/export/pdf/", export_ratings_pdf, name="export_ratings_pdf"),
]

