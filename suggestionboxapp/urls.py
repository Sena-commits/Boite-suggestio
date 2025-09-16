from django.urls import path
from . import views

app_name = 'suggestionboxapp'

urlpatterns = [
    # Categories
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/<uuid:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    
    # Suggestions
    path('suggestions/', views.SuggestionListCreateView.as_view(), name='suggestion-list'),
    path('suggestions/<uuid:pk>/', views.SuggestionDetailView.as_view(), name='suggestion-detail'),
    
    # Suggestions anonymes
    path('suggestions/anonymous/create/', views.create_anonymous_suggestion, name='anonymous-suggestion'),
    path('suggestions/track/<str:tracking_code>/', views.track_suggestion, name='track-suggestion'),
    
    # Votes
    path('suggestions/<uuid:pk>/vote/', views.vote_suggestion, name='vote-suggestion'),
    path('my-votes/', views.my_votes, name='my-votes'),
    
    # Commentaires
    path('suggestions/<uuid:pk>/comments/', views.add_comment, name='add-comment'),
    path('suggestions/<uuid:pk>/comments/list/', views.suggestion_comments, name='suggestion-comments'),
    
    # Statistiques
    path('stats/', views.public_stats, name='public-stats'),
    path('my-stats/', views.my_stats, name='my-stats'),
    
    # Modération
    path('suggestions/<uuid:pk>/status/', views.change_suggestion_status, name='change-status'),
    path('suggestions/<uuid:pk>/assign/', views.assign_suggestion, name='assign-suggestion'),
]