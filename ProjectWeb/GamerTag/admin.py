from django.contrib import admin
from .models import GameReview  # Importe o modelo que você criou

# Registre o modelo na interface administrativa
admin.site.register(GameReview)
