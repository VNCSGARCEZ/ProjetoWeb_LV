from django.views.generic import TemplateView
from django.shortcuts import render, redirect

# View para a página de login
class IndexView(TemplateView):
    template_name = "index.html"

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email == 'user@example.com' and password == 'password':
            return redirect('/home/')
        return self.get(request, *args, **kwargs)

# View para a página home
class HomeView(TemplateView):
    template_name = "home.html"

    def post(self, request, *args, **kwargs):
        game_name = request.POST.get('gameName')
        game_review = request.POST.get('gameReview')
        rating = request.POST.get('rating')
        game_image = request.FILES.get('gameImage')

        # Armazenar os dados na sessão
        if 'reviews' not in request.session:
            request.session['reviews'] = []

        # Criar um dicionário para armazenar as informações da análise
        review = {
            'game_name': game_name,
            'game_review': game_review,
            'rating': rating,
            'game_image': request.FILES.get('gameImage')  # Armazenar o arquivo
        }

        request.session['reviews'].append(review)
        request.session.modified = True

        return redirect('/analyze/')

# View para a página de análises
class AnalyzeView(TemplateView):
    template_name = "analyze.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.request.session.get('reviews', [])
        return context
