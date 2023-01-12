from django.urls import path

from quote import views

urlpatterns = [

    path('today', views.QuoteToday.as_view(), name="quote_today"),
    path('', views.QuoteList.as_view(), name='quote_list'),
    path('<int:id>', views.QuoteSingle.as_view(), name='quote_single'),
]
