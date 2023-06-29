from django.db import models
from django.contrib.auth.models import User

class Entidade(models.Model):
    designacao = models.TextField()
    morada = models.TextField()
    codigo_postal = models.TextField()
    contacto_telefonico = models.TextField()
    email = models.EmailField()

    def __str__(self):
        return self.designacao

class Atividade(models.Model):
    designacao = models.TextField(blank=True)
    descricao = models.TextField(blank=True)
    image = models.ImageField(upload_to='stakeholders/img/Atividades', blank=True)
    custo = models.TextField(blank=True)
    pessoa_de_contato = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    entidade = models.ForeignKey(Entidade, on_delete=models.CASCADE)

    def __str__(self):
        return self.designacao

class Evento(Atividade):
    local = models.TextField(blank=True)
    gps = models.TextField(blank=True)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    objetivo = models.TextField(blank=True)
    publico_alvo = models.TextField(blank=True)
    data_inicio_inscricao = models.DateField()
    data_limite_inscricao = models.DateField()
    vagas = models.TextField(blank=True)
    TIPO_CHOICES = [
    ('C', 'Curso'),
    ('F', 'Formacao'),
    ('CO', 'Congresso'),
    ('PA', 'Palestra'),
    ('SE', 'Seminario'),
    ('CN', 'Concurso'),
]
    tipoevento = models.CharField(max_length=2, choices=TIPO_CHOICES)

    def __str__(self):
        return f"Evento: {self.designacao}"

class Formacao(Evento):
    TIPO_CHOICES = [
    ('PG', 'PosGraduacao'),
    ('LI', 'Licenciatura'),
    ('ME', 'Mestrado'),
    ('DO', 'Doutoramento'),
    ('OU', 'Outros'),

]
    tipo = models.CharField(max_length=2, choices=TIPO_CHOICES)
    TIPO_ALUNO_CHOICES = [
        ('IJ', 'ImpulsoJovem'),
        ('IA', 'ImpulsoAdulto'),
        ('AM', 'Ambos'),
    ]
    tipo_de_aluno = models.CharField(max_length=2, choices=TIPO_ALUNO_CHOICES)
    ects = models.TextField(blank=True)

    def __str__(self):
        return f"Formacao: {self.designacao}"

class Participante(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nomes_do_meio = models.TextField(blank=True)
    data_nascimento = models.DateField(blank=True)
    nif = models.TextField(blank=True)
    morada = models.TextField(blank=True)
    codigo_postal = models.TextField(blank=True)
    freguesia = models.TextField(blank=True)
    concelho = models.TextField(blank=True)
    distrito = models.TextField(blank=True)
    contacto = models.TextField(blank=True)
    atividades = models.ManyToManyField(Evento, through='PreInscricao')

    def __str__(self):
        return self.user.username

class PreInscricao(models.Model):
    participante = models.ForeignKey(Participante, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    data_pre_inscricao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"PreInscricao - {self.participante.user.username} - {self.evento.atividade.designacao}"


class Stakeholder(models.Model):
    nome = models.TextField(blank=True)
    morada = models.TextField(blank=True)
    codigo_postal = models.TextField(blank=True)
    contacto_telefonico = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    pessoa_de_contato = models.TextField(blank=True)
    entidade = models.ForeignKey(Entidade, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome
    
class PessoasDeContato(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contato_telefonico = models.TextField(blank=True)
    stakeholder = models.ForeignKey(Stakeholder, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Servico(Atividade):
    detalhes = models.TextField(blank=True)

    def __str__(self):
        return f"Servico: {self.designacao}"

class Portefolio(models.Model):
    stakeholder = models.ForeignKey(Stakeholder, on_delete=models.CASCADE)
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    data_de_inicio = models.DateField()
    data_de_fim = models.DateField()
    imagens_de_referencia = models.ImageField(upload_to='stakeholders/img/Servicos', blank=True)
    detalhes = models.TextField(blank=True)
    publico = models.BooleanField(blank=True)
    data_de_requisicao = models.DateField()

    def __str__(self):
        return f"Portefolio ({self.stakeholder.nome} - {self.servico.designacao})"




