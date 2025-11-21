# monografias/urls.py
from django.urls import path
from . import views
from rest_framework import viewsets, permissions, filters
from .models import Monografia, Banca
from users.models import Professor
from .serializers import (
    MonografiaSerializer, 
    BancaSerializer, 
    ProfessorSerializer,
    MonografiaAprovadaSerializer
)
from django.utils import timezone

urlpatterns = [
    path('submeter/', views.submeter_monografia, name='submeter_monografia'),
    path('detalhe/<int:pk>/', views.detalhe_monografia, name='detalhe_monografia'),
    path('editar/<int:pk>/', views.editar_monografia, name='editar_monografia'),
    path('excluir/<int:pk>/', views.excluir_monografia, name='excluir_monografia'),
]

class ProfessorPublicViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Endpoint público (somente leitura) para listar Professores Orientadores[cite: 44].
    Permite ordenação.
    """
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = [permissions.AllowAny] # Público
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['nome', 'area_pesquisa'] # Permite ordenação 

class MonografiaPublicViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Endpoint público (somente leitura) para listar Monografias Aprovadas[cite: 43].
    """
    # Filtra apenas monografias com status 'APROVADO'
    queryset = Monografia.objects.filter(status='APROVADO')
    serializer_class = MonografiaAprovadaSerializer
    permission_classes = [permissions.AllowAny] # Público
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['data_defesa', 'titulo', 'autor__nome'] # Permite ordenação 

class MonografiaRestrictedViewSet(viewsets.ModelViewSet):
    """
    Endpoint restrito (CRUD via autenticação) para gerenciar Monografias[cite: 47].
    """
    queryset = Monografia.objects.all()
    serializer_class = MonografiaSerializer
    # Requer que o usuário esteja autenticado para qualquer ação
    permission_classes = [permissions.IsAuthenticated] 
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['data_criacao', 'titulo', 'status'] # Permite ordenação 

    def get_queryset(self):
        # Um usuário "Aluno" só pode ver/editar suas próprias monografias
        user = self.request.user
        if hasattr(user, 'aluno'):
            return Monografia.objects.filter(autor=user.aluno)
        # Professores ou Admins (staff) veem tudo
        elif user.is_staff:
            return Monografia.objects.all()
        # Caso de usuário autenticado sem perfil (não deve acontecer)
        return Monografia.objects.none()

class BancaRestrictedViewSet(viewsets.ModelViewSet):
    """
    Endpoint restrito (CRUD) para agendar defesas e registrar notas[cite: 48].
    """
    queryset = Banca.objects.all()
    serializer_class = BancaSerializer
    # Apenas usuários autenticados (idealmente Professores ou Admins) podem gerenciar bancas
    permission_classes = [permissions.IsAuthenticated] 

    def perform_create(self, serializer):
        # Ao criar a banca, atualiza a monografia associada
        banca = serializer.save()
        monografia = banca.monografia
        monografia.data_defesa = banca.data_defesa
        monografia.save()

    def perform_update(self, serializer):
        # Ao atualizar a banca (ex: registrar nota), atualiza a monografia
        banca = serializer.save()
        monografia = banca.monografia
        
        # Atualiza data da defesa na monografia
        if banca.data_defesa:
            monografia.data_defesa = banca.data_defesa

        # Se uma nota final foi registrada, atualiza o status da monografia
        if banca.nota_final is not None:
            if banca.nota_final >= 6.0:
                monografia.status = 'APROVADO'
            else:
                monografia.status = 'REPROVADO'
        
        monografia.save()