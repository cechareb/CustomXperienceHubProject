from django.contrib import admin
from .models import Post, Comentario

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('titulo','slug','autor','publicar','status')
    list_filter = ('status','creado','publicar','autor')
    search_fields = ('titulo','cuerpo')
    prepopulated_fields = {'slug': ('titulo',)}
    raw_id_fields = ('autor',)
    date_hierarchy = 'publicar'
    ordering = ('status','publicar')

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'post', 'creado', 'activo')
    list_filter = ('activo', 'creado', 'actualizado')
    search_fields = ('nombre', 'email', 'cuerpo')