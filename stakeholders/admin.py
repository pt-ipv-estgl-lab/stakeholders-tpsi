from django.contrib import admin
from .models import UnidadeOrganica, AtividadeFormativa, EventoCientifico, Servico, Profile, Participante, Inscricao
# Register your models here.
admin.site.register(UnidadeOrganica)
admin.site.register(AtividadeFormativa)
admin.site.register(EventoCientifico)
admin.site.register(Servico)
admin.site.register(Profile)
admin.site.register(Participante)
admin.site.register(Inscricao)
