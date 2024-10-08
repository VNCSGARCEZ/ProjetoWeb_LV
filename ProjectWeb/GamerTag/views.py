from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from PIL import Image  # Biblioteca para manipulação de imagens


class IndexView(TemplateView):
    template_name = "index.html"

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email == 'user@example.com' and password == 'password':
            return redirect('/home/')
        return self.get(request, *args, **kwargs)


class HomeView(TemplateView):
    template_name = "home.html"

    def post(self, request, *args, **kwargs):
        game_name = request.POST.get('gameName')
        game_review = request.POST.get('gameReview')
        rating = request.POST.get('rating')
        game_image = request.FILES.get('gameImage')


        if game_image:
            img = Image.open(game_image)
            max_width, max_height = 600, 900
            if img.width > max_width or img.height > max_height:

                return render(request, 'home.html', {
                    'error_message': f'A imagem deve ter no máximo {max_width}x{max_height} pixels.',
                })


        if 'reviews' not in request.session:
            request.session['reviews'] = []


        review = {
            'game_name': game_name,
            'game_review': game_review,
            'rating': rating,
            'game_image': game_image.name if game_image else None  # Armazenar o nome do arquivo
        }

        request.session['reviews'].append(review)
        request.session.modified = True

        return redirect('/analyze/')


class AnalyzeView(TemplateView):
    template_name = "analyze.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.request.session.get('reviews', [])
        return context


def delete_review(request, review_id):
    if 'reviews' in request.session:
        reviews = request.session['reviews']
        if 0 <= review_id < len(reviews):
            del reviews[review_id]
            request.session.modified = True
    return redirect('/analyze/')
