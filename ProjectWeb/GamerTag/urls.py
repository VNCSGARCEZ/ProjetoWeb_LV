from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import IndexView, HomeView, AnalyzeView

urlpatterns = [
    path('', IndexView.as_view(), name='inicio'),
    path('home/', HomeView.as_view(), name='home'),
    path('analyze/', AnalyzeView.as_view(), name='analyze'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
