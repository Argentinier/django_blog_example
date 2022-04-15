from django.contrib.postgres.search import SearchVector
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic import ListView
from taggit.models import Tag

from .forms import EmailPostForm, CommentForm, SearchForm
from .models import Post


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_share(request, post_id):
    # Retrieve Post by ID
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)

        if form.is_valid():
            cleaned_data = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"Read this: {post.title}"
            sent = bool(send_mail(
                subject=subject,
                message=f"{cleaned_data['email']} sent you this post {post_url}",
                from_email='system@my_site.com',
                recipient_list=[cleaned_data['to']],
                fail_silently=False))

    else:
        form = EmailPostForm()

    return render(
        request=request,
        template_name='blog/post/share.html',
        context={'post': post, 'form': form, 'sent': sent}
    )


def post_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)

        if form.is_valid():
            query = form.cleaned_data['query']
            search = SearchVector('title', 'body')
            results = Post.published.annotate(search=search).filter(search=query)

    return render(
        request=request,
        template_name='blog/post/search.html',
        context={
            'form': form,
            'query': query,
            'results': results
        }
    )


def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = Post.published.filter(tags__in=[tag])

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
            'posts': posts,
            'tag': tag
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

    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()

    else:
        comment_form = CommentForm()

    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    return render(
        request=request,
        template_name='blog/post/detail.html',
        context={
            'post': post,
            'comments': comments,
            'new_comment': new_comment,
            'comment_form': comment_form,
            'similar_posts': similar_posts
        }
    )
