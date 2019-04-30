from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, Comment
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm, SearchForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
from haystack.query import SearchQuerySet

# Create your views here.


def post_list(request, tag_slug=None):
    posts = Post.published.all()

    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])

    paginator = Paginator(posts, 3)  # 3 posts in each page
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # if page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    template = 'blog/post/list.html'
    context = {
        'posts': posts,
        'page': page,
        'tag': tag
    }
    return render(request, template_name=template, context=context)


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post, slug=slug,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             )

    # list of active comments for this post
    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        # a comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # create a comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the post to the comment
            new_comment.post = post
            # save the comment to the database
            new_comment.save()
            # clear out the comment form
            comment_form = CommentForm()

    else:
        comment_form = CommentForm()

    post_tags_id = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_id).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', 'publish')[:4]

    template = 'blog/post/detail.html'
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'similar_posts': similar_posts,
    }
    return render(request, template_name=template, context=context)


def post_share(request, post_id):
    # retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        # form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            name = cd['name']
            email = cd['email']
            to = cd['to']
            comment = cd['comments']
            post_title = post.title
            subject = f'{name} ({email}) recommends you reading "{post_title}"'
            message = f'Read "{post_title}" at {post_url}\n\n{name}\'s comments: {comment}'
            send_mail(subject, message, 'admin@myblog.com', [to])
            sent = True

    else:
        form = EmailPostForm()

    template = 'blog/post/share.html'
    context = {
        'post': post,
        'form': form,
        'sent': sent,
    }
    return render(request, template_name=template, context=context)


def post_search(request):
    form = SearchForm()
    template = 'blog/post/search.html'
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            results = SearchQuerySet().models(Post).filter(content=cd['query']).load_all()
            # count total results
            total_results = results.count()

            context = {'form': form, 'cd': cd, 'results': results, 'total_results': total_results}
            return render(request, template_name=template, context=context)

    return render(request, template_name=template, context={'form': form})
