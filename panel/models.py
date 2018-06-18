from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status='publicado')

class Post(models.Model):
    STATUS_CHOICES = (
        ('borrador','Borrador'),
        ('publicado','Publicado'),
    )
    titulo = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publicar')
    autor = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name='panel_posts')
    cuerpo = models.TextField()
    publicar = models.DateTimeField(default=timezone.now)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')
    objetos = models.Manager()
    publicado = PublishedManager()

    class Meta:
        ordering = ('-publicar',)

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse('panel:post_detail',
                           args=[self.publicar.year,
                             self.publicar.month,
                             self.publicar.day,
                             self.slug])

class Comentario(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comentarios')
    nombre = models.CharField(max_length=80)
    email = models.EmailField()
    cuerpo = models.TextField()
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ('creado',)

    def __str__(self):
        return 'Comentado por {} en {}'.format(self.nombre, self.post)