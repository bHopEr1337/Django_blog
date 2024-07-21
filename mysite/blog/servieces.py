from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Count

from .forms import CommentForm, SearchForm, EmailPostForm
from .models import Post

def __make_data_to_json_to_filter_posts(posts):
    """Возвращает json с информацией о постах"""
    data = {
        'posts': [
            {
                'id': post.id,
                'slug': post.slug,
                'title': post.title,
                'publish': post.publish,
                'author': post.author.username,
                'body': post.body,
                'category': post.category,
                'url': post.get_absolute_url(),

            } for post in posts
        ]
    }
    return JsonResponse(data)


def __get_detail_about_post(Model, year, month, day, post):
    """ Возвращает пост, форму, схожие посты и комментарии к этому посту """
    post = get_object_or_404(Model,
                             status=Model.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    comments = post.comments.filter(active=True)
    form = CommentForm()

    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = (Post.published.filter(tags__in=post_tags_ids) \
                     .exclude(id=post.id))
    similar_posts = similar_posts.annotate(same_tags=Count('tags')) \
                        .order_by('-same_tags', '-publish')[:4]

    return {'form': form, 'post': post, 'similar_posts': similar_posts, 'comments': comments}


def __add_and_save_comment_from_CommentForm(request, post_id):
    """ Добавление в пост комментов """
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()

    return {'form': form, 'comment': comment, 'post': post}


def find_posts_by_query(query):
    search_vector = SearchVector('title', weight='A', config='russian') + \
                    SearchVector('body', weight='B', config='russian')
    search_query = SearchQuery(query)

    return Post.published.annotate(
        search=search_vector,
        rank=SearchRank(search_vector, search_query)
    ).filter(rank__gte=0.3).order_by('-rank')


def __do_post_share_logic(request, post):
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
                      f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'pkuslin9@gmail.com',
                      [cd['to']])
            sent = True
    else:
        form = EmailPostForm()

    return {'post': post, 'form': form, 'sent': sent}
