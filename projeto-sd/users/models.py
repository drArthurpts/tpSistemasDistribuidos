# users/models.py
from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=200, null=True, blank=True)
    
    class Meta:
        abstract = True

    def __str__(self):
        return self.user.email

class Aluno(Perfil):
    matricula = models.CharField(max_length=20, unique=True)

class Professor(Perfil):
    TITULACAO_CHOICES = (
        ('DR', 'Doutor'),
        ('ME', 'Mestre'),
    )
    titulacao = models.CharField(max_length=2, choices=TITULACAO_CHOICES)
    area_pesquisa = models.CharField(max_length=100)