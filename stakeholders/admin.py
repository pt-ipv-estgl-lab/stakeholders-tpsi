from django.contrib import admin
from .models import Entidade, Servico, Evento, Participante, PreInscricao, PessoasDeContato, Formacao, Portefolio, Stakeholder
# Register your models here.
admin.site.register(Entidade)
admin.site.register(Servico)
admin.site.register(Evento)
admin.site.register(Formacao)
admin.site.register(Participante)
admin.site.register(PessoasDeContato)
admin.site.register(PreInscricao)
admin.site.register(Portefolio)
admin.site.register(Stakeholder)
