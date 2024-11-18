from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from PIL import Image  # Biblioteca para manipulação de imagens
from .models import GameReview  # Importa o modelo GameReview

# View para a página de login
class IndexView(TemplateView):
    template_name = "index.html"

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email == 'user@example.com' and password == 'password':
            return redirect('/home/')
        return self.get(request, *args, **kwargs)

# View para a página home - salva dados no banco de dados
class HomeView(TemplateView):
    template_name = "home.html"

    def post(self, request, *args, **kwargs):
        game_name = request.POST.get('gameName')
        game_review = request.POST.get('gameReview')
        rating = request.POST.get('rating')
        game_image = request.FILES.get('gameImage')

        # Verificação do tamanho da imagem
        if game_image:
            img = Image.open(game_image)
            max_width, max_height = 600, 900
            if img.width > max_width or img.height > max_height:
                # Se a imagem exceder o tamanho permitido, retorna a página com mensagem de erro
                return render(request, 'home.html', {
                    'error_message': f'A imagem deve ter no máximo {max_width}x{max_height} pixels.',
                })

        # Verificação dos campos obrigatórios
        if not game_name or not game_review or not rating:
            return render(request, 'home.html', {
                'error_message': 'Todos os campos são obrigatórios!',
            })

        if len(game_review) > 1000:
            return render(request, 'home.html', {
                'error_message': 'A análise não pode ter mais de 1000 caracteres.',
            })

        # Salvar os dados no banco de dados usando o modelo GameReview
        GameReview.objects.create(
            game_name=game_name,
            game_review=game_review,
            game_rating=int(rating),
            image=game_image
        )

        # Redireciona para a página de análises
        return redirect('/analyze/')

# View para a página de análises - exibe as análises salvas no banco de dados
class AnalyzeView(TemplateView):
    template_name = "analyze.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Carregar as análises do banco de dados
        context['reviews'] = GameReview.objects.all()  # Obtém todas as análises do banco
        return context

# Função para excluir uma análise com base no ID do banco de dados
def delete_review(request, review_id):
    try:
        review = GameReview.objects.get(id=review_id)  # Busca a análise pelo ID
        review.delete()  # Exclui a análise
    except GameReview.DoesNotExist:
        pass  # Caso não encontre, não faz nada
    return redirect('/analyze/')

