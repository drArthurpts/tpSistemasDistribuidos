from django import forms
from allauth.account.forms import LoginForm, SignupForm, ResetPasswordForm
from django.contrib.auth.models import Group
from .models import Aluno, Professor

class MyCustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(MyCustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Seu e-mail institucional'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Senha'})
        if 'remember' in self.fields:
            self.fields['remember'].widget.attrs.update({'class': 'form-check-input'})


class MyCustomResetPasswordForm(ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(MyCustomResetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Digite o e-mail cadastrado'})


class MyCustomSignupForm(SignupForm):
    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Endereço de e-mail'})
    )

    nome_completo = forms.CharField(
        max_length=200,
        label="Nome Completo",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu nome como aparece nos documentos'})
    )

    perfil = forms.ChoiceField(
        choices=(('Aluno', 'Sou Aluno(a)'), ('Professor', 'Sou Professor(a)')),
        label="Eu sou",
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_perfil'})
    )

    matricula = forms.CharField(
        max_length=20,
        label="Número de Matrícula",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    titulacao = forms.ChoiceField(
        choices=Professor.TITULACAO_CHOICES,
        label="Titulação",
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    area_pesquisa = forms.CharField(
        max_length=100,
        label="Área de Pesquisa",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    # ⚠️ Correção: usar password1 e password2 (allauth espera esses nomes)
    password1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Crie uma senha forte'})
    )

    password2 = forms.CharField(
        label="Senha (novamente)",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirme sua senha'})
    )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As duas senhas não coincidem.")
        return password2

    def save(self, request):
        # Chama o save do SignupForm (cria o usuário e seta a senha)
        user = super(MyCustomSignupForm, self).save(request)

        perfil_selecionado = self.cleaned_data.get('perfil')
        nome = self.cleaned_data.get('nome_completo')

        # Adiciona em grupos e cria perfil extra
        if perfil_selecionado == 'Aluno':
            grupo = Group.objects.get(name='Alunos')
            user.groups.add(grupo)
            Aluno.objects.create(
                user=user,
                nome_completo=nome,
                matricula=self.cleaned_data.get('matricula')
            )

        elif perfil_selecionado == 'Professor':
            grupo = Group.objects.get(name='Professores Pendentes')
            user.groups.add(grupo)
            Professor.objects.create(
                user=user,
                nome_completo=nome,
                titulacao=self.cleaned_data.get('titulacao'),
                area_pesquisa=self.cleaned_data.get('area_pesquisa')
            )

        return user
