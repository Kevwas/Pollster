from django.urls import path

from . import views

app_name = 'polls'
# urlpatterns = [
#     # ex: /polls/
#     path('', views.index, name='index'),
#     # ex: /polls/5/
#     path('<int:question_id>/', views.detail, name='detail'),
#     # ex: /polls/5/results/
#     path('<int:question_id>/results/', views.results, name='results'),
#     # ex: /polls/5/vote/
#     path('<int:question_id>/vote/', views.vote, name='vote'),
# ]

# Use generic views: Less code is better
urlpatterns = [
    path('polls/', views.PollsView.as_view(), name='polls'),
    path('polls/<int:pk>/detail', views.DetailView.as_view(), name='detail'),
    path('polls/<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # path('polls/create/', views.CreatePollsView.as_view(), name='create'),
    # path('polls/<int:pk>/addchoice/', views.AddChoicesView.as_view(), name='addChoice'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),

    path('polls/<int:question_id>/vote/', views.vote, name='vote'),
    path('resultsData/<str:obj>/', views.resultsData, name='resultsData'),
    
    path('', views.index, name='index'),
]
