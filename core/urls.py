from django.urls import path
from . import views

app_name = 'core'  # Namespace declaration

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('upload/', views.upload_research, name='upload'),  # Must exist
    path('summarize/<int:research_id>/',
         views.summarize_research,
         name='summarize'),
    path('summarize/<int:research_id>/stream/',
         views.stream_summary,
         name='stream-summary'),
    path('translate/', views.translate_text, name='translate'),
]