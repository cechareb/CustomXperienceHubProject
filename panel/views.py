from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from .models import Post, Comentario
from .forms import EmailPostFormulario, ComentarioFormulario

def post_list(request):
    object_list=Post.publicado.all()
    paginator = Paginator(object_list, 3)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'panel/post/listar.html',
                  {'page': page,
                   'posts': posts})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                   status='publicado',
                                   publicar__year=year,
                                   publicar__month=month,
                                   publicar__day=day)

    comentarios = post.comentarios.filter(activo=True)
    nuevo_comentario = None

    if request.method == 'POST':
        comentario_formulario = ComentarioFormulario(data=request.POST)
        if comentario_formulario.is_valid():
            nuevo_comentario = comentario_formulario.save(commit=False)
            nuevo_comentario.post = post
            nuevo_comentario.save()
    else:
        comentario_formulario = ComentarioFormulario()
    return render(request,
                  'panel/post/detalle.html',
                  {'post': post,
                  'comentarios': comentarios,
                  'nuevo_comentario': nuevo_comentario,
                  'comentario_formulario':comentario_formulario})

class PostListView(ListView):
    queryset = Post.publicado.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'panel/post/listar.html'

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='publicado')
    enviado = False

    if request.method == 'POST':
        formulario = EmailPostFormulario(request.POST)
        if formulario.is_valid():
            cd = formulario.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) te recomienda leer "{}"'.format(cd['nombre'], cd['email'], post.titulo)
            message = 'Lea "{}" en los comentarios de {}\n\n{}\:{}'.format(post.titulo, post_url, cd['nombre'], cd['comentarios'])
            send_mail(subject, message, 'experiencia-cliente@entel.pe',[cd['para']])
            enviado = True
        else:
            formulario = EmailPostFormulario()
        return render(request, 'panel/post/compartir.html', {'post': post,
                                                        'formulario': formulario,
                                                        'enviado': enviado})
    else:
        formulario = EmailPostFormulario()
    return render(request, 'panel/post/compartir.html', {'post': post,
                                                         'formulario': formulario})