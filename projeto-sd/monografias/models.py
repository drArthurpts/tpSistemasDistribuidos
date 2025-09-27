# monografias/models.py
from django.db import models
from users.models import Aluno, Professor
from simple_history.models import HistoricalRecords

class Monografia(models.Model):
    STATUS_CHOICES = (
        ('EM_AVALIACAO', 'Em Avaliação'),
        ('APROVADO', 'Aprovado'),
        ('REPROVADO', 'Reprovado'),
        ('CORRECAO', 'Em Correção'),
    )

    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    orientador = models.ForeignKey(Professor, related_name='orientacoes', on_delete=models.SET_NULL, null=True)
    coorientador = models.ForeignKey(Professor, related_name='coorientacoes', on_delete=models.SET_NULL, null=True, blank=True)
    
    resumo = models.TextField()
    abstract = models.TextField()
    palavras_chave = models.CharField(max_length=255)

    documento_pdf = models.FileField(upload_to='monografias_pdf/')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='EM_AVALIACAO')
    data_defesa = models.DateField(null=True, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    history = HistoricalRecords()

    def __str__(self):
        return self.titulo

class Banca(models.Model):
    monografia = models.OneToOneField(Monografia, on_delete=models.CASCADE)
    avaliadores = models.ManyToManyField(Professor)
    data_defesa = models.DateTimeField()
    local_defesa = models.CharField(max_length=100)
    nota_final = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Banca de {self.monografia.titulo}"
