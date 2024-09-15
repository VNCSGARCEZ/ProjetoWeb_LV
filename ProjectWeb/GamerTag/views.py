from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.shortcuts import render

# View para a página de login
class IndexView(TemplateView):
    template_name = "index.html"  # Template da página de login

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Simulação de verificação de login (você pode implementar a lógica real aqui)
        if email == 'user@example.com' and password == 'password':
            return HttpResponseRedirect('/home/')  # Redireciona para a página home após login bem-sucedido
        return self.get(request, *args, **kwargs)  # Se o login falhar, recarrega a página de login

# View para a página home
class HomeView(TemplateView):
    template_name = "home.html"  # Template da página home
