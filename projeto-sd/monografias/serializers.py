from rest_framework import serializers
from .models import Monografia, Banca
from users.models import Professor, Aluno

class ProfessorSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Professor

        fields = ['id', 'nome_completo', 'email', 'titulacao', 'area_pesquisa']

class AlunoSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Aluno

        fields = ['id', 'nome_completo', 'matricula', 'email']

class MonografiaAprovadaSerializer(serializers.ModelSerializer):

    autor = AlunoSerializer(read_only=True)
    orientador = ProfessorSerializer(read_only=True)

    class Meta:
        model = Monografia

        fields = ['id', 'titulo', 'autor', 'orientador', 'data_defesa', 'resumo', 'status']

class MonografiaSerializer(serializers.ModelSerializer):

    autor = AlunoSerializer(read_only=True)
    orientador = ProfessorSerializer(read_only=True)
    coorientador = ProfessorSerializer(read_only=True, required=False)

    autor_id = serializers.PrimaryKeyRelatedField(
        queryset=Aluno.objects.all(), source='autor', write_only=True
    )
    orientador_id = serializers.PrimaryKeyRelatedField(
        queryset=Professor.objects.all(), source='orientador', write_only=True
    )
    coorientador_id = serializers.PrimaryKeyRelatedField(
        queryset=Professor.objects.all(), source='coorientador', write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = Monografia

        fields = [
            'id', 'titulo', 'autor', 'orientador', 'coorientador',
            'resumo', 'abstract', 'palavras_chave', 'documento_pdf',
            'status', 'data_defesa', 'data_criacao',
            'autor_id', 'orientador_id', 'coorientador_id'
        ]

        read_only_fields = ['status', 'data_criacao']

class BancaSerializer(serializers.ModelSerializer):

    monografia = MonografiaSerializer(read_only=True)
    avaliadores = ProfessorSerializer(many=True, read_only=True)

    monografia_id = serializers.PrimaryKeyRelatedField(
        queryset=Monografia.objects.all(), source='monografia', write_only=True
    )
    avaliadores_ids = serializers.PrimaryKeyRelatedField(
        queryset=Professor.objects.all(), source='avaliadores', write_only=True
    )

    class Meta:
        model = Banca
        fields = [
            'id', 'monografia', 'avaliadores', 'data_defesa', 
            'local_defesa', 'nota_final', 
            'monografia_id', 'avaliadores_ids'
        ]