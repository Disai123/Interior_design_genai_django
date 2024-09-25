from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_user),
    path('register/', views.register_user),
    path('genAIPrompt2/', views.genAIPrompt2),
    path('generateImage/', views.generateImage),
    path('donate/', views.donate),
]
