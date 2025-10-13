# users/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from monografias.models import Monografia
from django.db.models import Q

# View para a página principal/homepage
def home_view(request):
    return render(request, 'home.html')

# View para o dashboard do usuário
@login_required
def dashboard_view(request):
    is_aluno = request.user.groups.filter(name='Alunos').exists()
    is_professor = request.user.groups.filter(name='Professores').exists()
    is_admin = request.user.groups.filter(name='Administradores').exists()
    
    # Nova verificação para o grupo de professores pendentes
    is_professor_pendente = request.user.groups.filter(name='Professores Pendentes').exists()

    # Usuário genérico aguardando aprovação (não está em nenhum grupo principal)
    aguardando_aprovacao = not (is_aluno or is_professor or is_admin or is_professor_pendente)

    context = {
        'user': request.user,
        'is_aluno': is_aluno,
        'is_professor': is_professor,
        'is_admin': is_admin,
        'is_professor_pendente': is_professor_pendente,
        'aguardando_aprovacao': aguardando_aprovacao,
    }

    if is_professor:
        try:
            professor_profile = request.user.professor
            
            monografias_orientadas = Monografia.objects.filter(
                Q(orientador=professor_profile) | Q(coorientador=professor_profile)
            ).distinct().order_by('-data_criacao')
            
            context['monografias_orientadas'] = monografias_orientadas

        except request.user._meta.model.professor.RelatedObjectDoesNotExist:
            context['monografias_orientadas'] = []

    if is_aluno:
        try:
            aluno_profile = request.user.aluno
            minhas_monografias = Monografia.objects.filter(autor=aluno_profile).order_by('-data_criacao')
            context['minhas_monografias'] = minhas_monografias
        except Exception:
            context['minhas_monografias'] = []

    return render(request, 'dashboard.html', context)