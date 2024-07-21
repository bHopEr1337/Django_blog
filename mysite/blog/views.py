from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.views.decorators.http import require_POST

from .servieces import __make_data_to_json_to_filter_posts, __get_detail_about_post, \
    __add_and_save_comment_from_CommentForm, find_posts_by_query, __do_post_share_logic
from .models import Post
from .forms import EmailPostForm, SearchForm


def post_list(request, tag_slug=None):
    posts = Post.published.all()
    return render(request,
                  'blog/post/list2.html',
                  context={'posts':posts})

def greeting(request):
    return render(request, template_name='blog/post/greeting.html')

def about(request):
    return render(request, template_name='blog/post/about.html')


def send_feedback(request):
    return render(request, 'blog/post/send_feedback.html')


def filter_posts(request):
    category = request.GET.get('category')
    if category:
        posts = Post.objects.filter(category=category)
    else:
        posts = Post.objects.all()

    return __make_data_to_json_to_filter_posts(posts)


def post_detail(request, year, month, day, post):
    post_detail_data = __get_detail_about_post(Post, year, month, day, post)

    return render(request,
                  'blog/post/detail.html',
                  {'post': post_detail_data['post'],
                          'comments': post_detail_data['comments'],
                          'form': post_detail_data['form'],
                          'similar_posts': post_detail_data['similar_posts']})


@require_POST
def post_comment(request, post_id):
    data = __add_and_save_comment_from_CommentForm(request, post_id)
    return render(request, 'blog/post/comment.html',
                  {'post': data['post'],
                   'form': data['form'],
                   'comment': data['comment'],})

def post_search_view(request):
    form = SearchForm(request.GET or None)
    query = None
    results = []

    if form.is_valid():
        query = form.cleaned_data['query']
        results = find_posts_by_query(query)

    return render(request, 'blog/post/search.html', {
        'form': form,
        'query': query,
        'results': results
    })


def post_share(request, post_id):
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)
    data = __do_post_share_logic(request, post)

    return render(request, 'blog/post/share.html', {'post':data['post'],
                                                                            'form':data['form'],
                                                                            'sent':data['sent']})