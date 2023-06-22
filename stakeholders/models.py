from django.db import models
from django.contrib.auth.models import User

class UnidadeOrganica(models.Model):
    nome = models.TextField()
    morada = models.TextField()
    contacto = models.TextField()
    email = models.TextField()

    def __str__(self):
        return self.nome
      
      
class Atividade(models.Model):
    AREAS_ATIVIDADE = (
        ('Saúde', 'Saúde'),
        ('Tecnologia', 'Tecnologia'),
        ('Agricultura', 'Agricultura'),
        ('Educação', 'Educação'),
    	  ('Matemática', 'Matemática'),
	      ('Outras', 'Outras'),
    )

    nome = models.TextField()
    descricao = models.TextField()
    image = models.ImageField(upload_to='stakeholders/img/Atividades', blank=True)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    area = models.CharField(max_length=20, choices=AREAS_ATIVIDADE,default='Tecnologia') 
    local = models.TextField(blank=True)
    objetivos = models.TextField(blank=True)
    custos = models.TextField(blank=True)
    publico_alvo = models.TextField(blank=True)
    contacto = models.TextField(blank=True)
    email = models.TextField(blank=True)
    unidade_organica = models.ForeignKey(UnidadeOrganica, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class AtividadeFormativa(Atividade):
    TIPOS_ATIVIDADE = (
        ('C', 'Curso'),
        ('F', 'Formacao'),
    )
    data_limite_inscricao = models.DateField()
    responsavel = models.TextField()
    tipodeatividade = models.CharField(max_length=2, choices=TIPOS_ATIVIDADE,default='C')
    certificacao = models.TextField(blank=True)
    programa = models.TextField(blank=True)
    duracao = models.TextField(blank=True)
    vagas = models.TextField(blank=True)
    edicao = models.TextField(blank=True)
    requisitos = models.TextField(blank=True)
    horario = models.TextField(blank=True)
    fases = models.TextField(blank=True)
    regime = models.TextField(blank=True)

    def __str__(self):
        return self.nome

class EventoCientifico(Atividade):
    TIPOS_EVENTO = (
        ('CO', 'Congresso'),
        ('PA', 'Palestra'),
        ('SE', 'Seminario'),
        ('CN', 'Concurso'),
    )

    tipodeevento = models.CharField(max_length=2, choices=TIPOS_EVENTO,default='CO')
    data_limite_inscricao = models.DateField()
    programa = models.TextField(blank=True)
    duracao = models.TextField(blank=True)
    vagas = models.TextField(blank=True)
    horario = models.TextField(blank=True)
    agenda = models.TextField(blank=True)
    alojamento = models.TextField(blank=True)
    local_alojamento = models.TextField(blank=True)
    orador = models.TextField(blank=True)
    moderador = models.TextField(blank=True)
    data_submissao_resumos = models.TextField(blank=True)
    data_notificacao_resumos = models.TextField(blank=True)
    link = models.TextField(blank=True)
    parcerias = models.TextField(blank=True)
    numero_elementos_equipa = models.TextField(blank=True)

    def __str__(self):
        return self.nome

class Servico(Atividade):
    pass

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_completo = models.TextField(blank=True)
    nif = models.TextField(blank=True)
    morada = models.TextField(blank=True)
    codigo_postal = models.TextField(blank=True)
    freguesia = models.TextField(blank=True)
    concelho = models.TextField(blank=True)
    distrito = models.TextField(blank=True)
    contacto = models.TextField(blank=True)
    atividades = models.ManyToManyField(Atividade, through='Inscricao')

    def __str__(self):
        return self.user.username


class Participante(Profile):
    GENDER_CHOICES = (
        ('E', 'Escolha Uma'),
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro')
    )

    ACADEMIC_CHOICES = (
        ('E', 'Escolha Uma'),
        ('4', '4º ano'),
        ('9', '9º ano'),
        ('12', '12º ano'),
        ('L', 'Licenciatura'),
        ('M', 'Mestrado'),
        ('D', 'Doutoramento'),
    )

    EMPLOYMENT_CHOICES = (
        ('E', 'Escolha Uma'),
        ('ES', 'Estudante - Secundário'),
        ('EL', 'Estudante - Licenciatura'),
        ('EO', 'Estudante - Outra'),
        ('TP', 'Trabalhador por conta própria'),
        ('TO', 'Trabalhador por conta de outrem'),
        ('DE', 'Desempregado'),
        ('O', 'Outra'),
    )

    genero = models.CharField(max_length=1, choices=GENDER_CHOICES,default='E')
    nacionalidade = models.TextField()
    data_nascimento = models.DateField()
    formacao_academica = models.CharField(max_length=2, choices=ACADEMIC_CHOICES,default='E')
    atividade_profissional = models.CharField(max_length=2, choices=EMPLOYMENT_CHOICES,default='E')

    def __str__(self):
        return f"Participante: {self.user.username}"

class Inscricao(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    atividade = models.ForeignKey(Atividade, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inscrição: {self.pk}"



