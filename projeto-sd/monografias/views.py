from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import MonografiaForm
from users.models import Aluno 
from .models import Monografia

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

@login_required
def submeter_monografia(request):
    try:
        aluno = request.user.aluno
    except Aluno.DoesNotExist:
        return redirect('dashboard') 

    if request.method == 'POST':
        form = MonografiaForm(request.POST, request.FILES)
        if form.is_valid():
            monografia = form.save(commit=False)
            
            monografia.autor = aluno
           
            monografia.save()
        
            return redirect('dashboard')
    else:
        form = MonografiaForm()

    context = {
        'form': form
    }
    return render(request, 'monografias/submeter.html', context)


@login_required
def detalhe_monografia(request, pk):
    monografia = get_object_or_404(Monografia, pk=pk)
    
    context = {
        'monografia': monografia
    }
    return render(request, 'monografias/detalhe_monografia.html', context)

# monografias/views.py

@login_required
def editar_monografia(request, pk):
    monografia = get_object_or_404(Monografia, pk=pk)
    is_autor = (request.user == monografia.autor.user)
    is_orientador = False
    try:
        if request.user.professor == monografia.orientador:
            is_orientador = True
    except Exception:
        pass

    if not (is_autor or is_orientador or request.user.is_superuser):
        return redirect('dashboard') 

    if request.method == 'POST':
        form = MonografiaForm(request.POST, request.FILES, instance=monografia)
        if form.is_valid():
            form.save()
            return redirect('detalhe_monografia', pk=monografia.pk)
    else:
        form = MonografiaForm(instance=monografia)

    context = {
        'form': form,
        'monografia': monografia
    }
    return render(request, 'monografias/editar_monografia.html', context)

@login_required
def excluir_monografia(request, pk):
    monografia = get_object_or_404(Monografia, pk=pk)

    if not (request.user == monografia.autor.user or request.user.is_superuser or request.user == monografia.orientador.user):
        return redirect('dashboard')

    if request.method == 'POST':
        monografia.delete()
        return redirect('listar_monografias')

    context = {
        'monografia': monografia
    }
    return render(request, 'monografias/excluir_monografia.html', context)

class ProfessorPublicViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Endpoint público (somente leitura) para listar Professores Orientadores.
    """
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = [permissions.AllowAny] 
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['nome', 'area_pesquisa']

class MonografiaPublicViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Endpoint público (somente leitura) para listar Monografias Aprovadas.
    """
    queryset = Monografia.objects.filter(status='APROVADO')
    serializer_class = MonografiaAprovadaSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['data_defesa', 'titulo', 'autor__nome']

class MonografiaRestrictedViewSet(viewsets.ModelViewSet):
    """
    Endpoint restrito (CRUD via autenticação) para gerenciar Monografias.
    """
    queryset = Monografia.objects.all()
    serializer_class = MonografiaSerializer
    permission_classes = [permissions.IsAuthenticated] 
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['data_criacao', 'titulo', 'status']

    def get_queryset(self):
        # ... (lógica de permissão de acesso aqui) ...
        user = self.request.user
        if hasattr(user, 'aluno'):
            return Monografia.objects.filter(autor=user.aluno)
        elif user.is_staff:
            return Monografia.objects.all()
        return Monografia.objects.none()

class BancaRestrictedViewSet(viewsets.ModelViewSet):
    """
    Endpoint restrito (CRUD) para agendar defesas e registrar notas.
    """
    queryset = Banca.objects.all()
    serializer_class = BancaSerializer
    permission_classes = [permissions.IsAuthenticated] 

    def perform_create(self, serializer):
        # ... (lógica de criação e atualização de status) ...
        banca = serializer.save()
        monografia = banca.monografia
        monografia.data_defesa = banca.data_defesa
        monografia.save()

    def perform_update(self, serializer):
        # ... (lógica de atualização e registro de nota) ...
        banca = serializer.save()
        monografia = banca.monografia
        
        if banca.data_defesa:
            monografia.data_defesa = banca.data_defesa

        if banca.nota_final is not None:
            if banca.nota_final >= 6.0: 
                monografia.status = 'APROVADO'
            else:
                monografia.status = 'REPROVADO'
        
        monografia.save()