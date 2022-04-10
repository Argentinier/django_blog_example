from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class TimestampsMixin(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Post(TimestampsMixin):

    # It's good practice declaring inside the class you can access Post.DRAFT anywhere you have imported Post
    # Also important to have the 'Keys' outside the CHOICES tuple, so you can use them for the default property
    DRAFT = 'draft'
    PUBLISHED = 'published'

    # An iterable of tuples with 2 values.
    # First value is the Key stored in the Model, second is the human-readable value.
    # If 'None' is set it replaces the '-------'. But in this case I'm using a default, so doesn't matter anyway.
    STATUS_CHOICES = (
        ('None', 'Select the Post Status'),
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published')
    )

    title = models.CharField(max_length=250)

    # unique_for_date means only one slug with the same name will be allowed per day
    slug_name = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField(max_length=5000)
    publish = models.DateTimeField(default=timezone.now)

    # By defining choices this CharField only can accept the values given by the choices iterable
    # You can access to the readable part of the choice in this case like 'post.get_status_display()'
    status = models.CharField(max_length=250, choices=STATUS_CHOICES, default=DRAFT)

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title
