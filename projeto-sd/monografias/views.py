from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import MonografiaForm
from users.models import Aluno 
from .models import Monografia

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