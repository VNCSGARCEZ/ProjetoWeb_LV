from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import IndexView, HomeView, AnalyzeView, delete_review, RegisterView, user_logout, update_review


urlpatterns = [
    # Rota para a página inicial (Login)
    path('', IndexView.as_view(), name='inicio'),

    # Rota para a página de cadastro
    path('cadastro/', RegisterView.as_view(), name='cadastro'),

    # Rota para a página inicial após login
    path('home/', HomeView.as_view(), name='home'),

    # Rota para a página de análises
    path('analyze/', AnalyzeView.as_view(), name='analyze'),

    # Rota para deletar uma análise
    path('delete_review/<int:review_id>/', delete_review, name='delete_review'),

    path('update_review/<int:review_id>/', update_review, name='update_review'),

    # Rota para logout
    path('logout/', user_logout, name='logout'),
]

# Adiciona suporte a arquivos de mídia em ambiente de desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
