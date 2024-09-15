from django.urls import path
from .views import IndexView, HomeView

urlpatterns = [
    path('', IndexView.as_view(), name='inicio'),  # Página de login será carregada como página inicial
    path('home/', HomeView.as_view(), name='home'),  # Página Home será carregada após o login
]
