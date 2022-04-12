from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404

# Create your views here.
from .models import Post


def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list=object_list, per_page=3)
    page = request.GET.get('page')

    try:
        # Retrieve the requested Page if valid
        posts = paginator.page(page)
    except PageNotAnInteger:
        # Retrieve first Page if page was not valid
        posts = paginator.page(1)
    except EmptyPage:
        # Retrieve last Page if page was greater than posible
        posts = paginator.page(paginator.num_pages)

    return render(
        request=request,
        template_name='blog/post/list.html',
        context={
            'page': page,
            'posts': posts
        }
    )


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        slug=post,
        status=Post.PUBLISHED,
        publish__year=year,
        publish__month=month,
        publish__day=day
    )

    return render(
        request=request,
        template_name='blog/post/detail.html',
        context={'post': post}
    )
