from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from PIL import Image  # Biblioteca para manipulação de imagens
from .models import GameReview  # Apenas importa GameReview

# View para a página de login
class IndexView(TemplateView):
    template_name = "index.html"

    def post(self, request, *args, **kwargs):
        # Se o usuário já estiver autenticado, não faz nada
        if request.user.is_authenticated:
            return redirect('/home/')  # Redireciona diretamente para o home

        email = request.POST.get('email')
        password = request.POST.get('password')

        # Autenticação do usuário - Usa o email para autenticação
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect('/home/')  # Redireciona para a página home após login

        # Caso a autenticação falhe
        return render(request, self.template_name, {
            'error_message': 'Email ou senha inválidos.'
        })

# Função para atualizar uma análise
@login_required
def update_review(request, review_id):
    try:
        review = GameReview.objects.get(id=review_id)  # Obtém a análise pelo ID
    except GameReview.DoesNotExist:
        return redirect('/analyze/')  # Redireciona caso a análise não exista

    if request.method == "POST":
        game_name = request.POST.get('gameName')
        game_review = request.POST.get('gameReview')
        rating = request.POST.get('rating')
        game_image = request.FILES.get('gameImage')

        # Validação dos campos
        if not game_name or not game_review or not rating:
            return render(request, 'update_review.html', {
                'error_message': 'Todos os campos são obrigatórios!',
                'review': review
            })

        if len(game_review) > 1000:
            return render(request, 'update_review.html', {
                'error_message': 'A análise não pode ter mais de 1000 caracteres.',
                'review': review
            })

        # Atualiza os dados da análise
        review.game_name = game_name
        review.game_review = game_review
        review.game_rating = int(rating)

        # Atualiza a imagem se uma nova for enviada
        if game_image:
            img = Image.open(game_image)
            max_width, max_height = 600, 900
            if img.width > max_width or img.height > max_height:
                return render(request, 'update_review.html', {
                    'error_message': f'A imagem deve ter no máximo {max_width}x{max_height} pixels.',
                    'review': review
                })
            review.image = game_image

        review.save()  # Salva as alterações no banco de dados
        return redirect('/analyze/')  # Redireciona para a página de análises

    return render(request, 'update_review.html', {'review': review})  # Renderiza o formulário de edição

# View para a página de cadastro
class RegisterView(TemplateView):
    template_name = "register.html"

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')  # Pode ser o email, caso queira
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Validação de senha
        if password != confirm_password:
            return render(request, self.template_name, {
                'error_message': 'As senhas não coincidem.'
            })

        # Verificar se o email já está registrado
        if User.objects.filter(email=email).exists():  # Agora você verifica pelo email
            return render(request, self.template_name, {
                'error_message': 'O email já está registrado.'
            })

        # Criar o usuário sem permissões de admin (não será superusuário)
        user = User.objects.create_user(username=email, email=email, password=password)
        # Remover permissões de admin
        user.is_staff = False  # Não será admin no Django
        user.is_superuser = False  # Não será superusuário no Django
        user.save()

        # Não faz login automático do novo usuário, para não desconectar o superusuário
        # login(request, user)  # Essa linha foi removida

        return redirect('/home/')  # Após o cadastro, redireciona para a página home


# View para a página home - salva dados no banco de dados
@method_decorator(login_required, name='dispatch')
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
                return render(request, self.template_name, {
                    'error_message': f'A imagem deve ter no máximo {max_width}x{max_height} pixels.',
                })

        # Verificação dos campos obrigatórios
        if not game_name or not game_review or not rating:
            return render(request, self.template_name, {
                'error_message': 'Todos os campos são obrigatórios!',
            })

        if len(game_review) > 1000:  # Limitar a análise a 1000 caracteres
            return render(request, self.template_name, {
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
@method_decorator(login_required, name='dispatch')
class AnalyzeView(TemplateView):
    template_name = "analyze.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Carregar as análises do banco de dados
        context['reviews'] = GameReview.objects.all()  # Obtém todas as análises do banco
        return context


# Função para excluir uma análise com base no ID do banco de dados
@login_required
def delete_review(request, review_id):
    try:
        review = GameReview.objects.get(id=review_id)  # Busca a análise pelo ID
        review.delete()  # Exclui a análise
    except GameReview.DoesNotExist:
        pass  # Caso não encontre, não faz nada
    return redirect('/analyze/')


# Função para logout
def user_logout(request):
    logout(request)  # Finaliza a sessão do usuário
