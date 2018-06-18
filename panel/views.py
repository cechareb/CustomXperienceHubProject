from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from .models import Post
from .forms import EmailPostFormulario

def post_list(request):
    object_list=Post.publicado.all()
    paginator = Paginator(object_list, 3)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
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
    return render(request,
                  'panel/post/detalle.html',
                  {'post':post})

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