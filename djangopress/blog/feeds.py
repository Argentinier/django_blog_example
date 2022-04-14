from typing import List

from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy
from .models import Post


class LatestPostFeed(Feed):
    title = 'My blog'
    description = 'These are the latest Posts in my Blog'
    link = reverse_lazy('blog:post_list')

    def items(self) -> List[Post]:
        return Post.published.all()[:5]

    def item_title(self, item: Post) -> str:
        return item.title

    def item_description(self, item: Post) -> str:
        return truncatewords(item.body, 30)
