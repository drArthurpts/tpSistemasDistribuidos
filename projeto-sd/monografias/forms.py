from django import forms
from .models import Monografia

class MonografiaForm(forms.ModelForm):
    class Meta:
        model = Monografia
    
        fields = [
            'titulo',
            'orientador',
            'coorientador',
            'resumo',
            'abstract',
            'palavras_chave',
            'documento_pdf',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        
        self.fields['orientador'].widget.attrs['class'] = 'form-select'
        self.fields['coorientador'].widget.attrs['class'] = 'form-select'