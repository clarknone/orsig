from django.urls import path

from record.views import RecordsView, CommitsView, RecordSingleView

urlpatterns = [
    path('', RecordsView.as_view(), name="records"),
    path('<int:id>', RecordSingleView.as_view(), name="record_single"),
    path('commit', CommitsView.as_view(), name="commit"),
]
