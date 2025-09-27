# monografias/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('submeter/', views.submeter_monografia, name='submeter_monografia'),
    path('detalhe/<int:pk>/', views.detalhe_monografia, name='detalhe_monografia'),
    path('editar/<int:pk>/', views.editar_monografia, name='editar_monografia'),
    path('excluir/<int:pk>/', views.excluir_monografia, name='excluir_monografia'),
]