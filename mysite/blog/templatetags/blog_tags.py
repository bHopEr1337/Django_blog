from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown


register = template.Library()

# Простой тег возвращает строковый литерал
@register.simple_tag
def total_posts():
    return Post.published.count()

# Тег включения возвращает прорисованный шаблон
# Главная фишка тега включения - возможность передавать опциональный параметр
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


# Данная функция возвращает набор объектов из модели пост
@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(
        total_comments=Count('comments')
    ).order_by('-total_comments')[:count]


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))


@register.filter
def truncatewords_html(value, arg):
    return truncatewords_html(value, arg)
