from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
from django.contrib.auth.models import User #adding many-to--one relationship
from django.urls import reverse #ch2 canonical urls
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset() \
                    .filter(status=Post.Status.PUBLISHED)

class Post(models.Model):
    # to save posts as drafts
    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    title = models.CharField(max_length=250)  # VARCHAR(250)
    slug = models.SlugField(max_length=250,unique_for_date='publish')  # VARCHAR(250) 
    '''ch2 SEO friendly URLs --  slug/ unique_for_date='publish' ensures that slug values are unique to the publication date'''

    #many-to-one 
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    
    body = models.TextField(max_length=250)  # TEXT
    publish = models.DateTimeField(default=timezone.now)  # DATETIME
    created = models.DateTimeField(auto_now_add=True)  # DATETIME
    updated = models.DateTimeField(auto_now=True)  # DATETIME

    # changes in respect 
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.DRAFT
    )

    objects = models.Manager()
    published = PublishedManager()

    class Meta:  # metadata for the Post class
        # default sort order
        ordering = ["-publish"]  #'-' for descending order

        # database index
        indexes = [
            models.Index(fields=["-publish"]),  # index for publish
        ]

    def __str__(self):
        return self.title
    
    #ch2 canonical urls
    def get_absolute_url(self):
        """ch2 canonical URLs
        returns the canonical URL for the object.
        Returns:
            _URL string_: _reverse() will build the URL dynamically using the URL name defined in the URL patterns. 
            blog:post_detail can be used globally in the project to refer to the post detail URL. 
            id refers to the id of the Post object. It is a required parameter which retrieves the blog post. _
        """

        '''ch2 SEO friendly URLs
        we change the args parameters to match the new URL parameters.
        '''
        return reverse('blog:post_detail',args=[self.publish.year,self.publish.month,self.publish.day,self.slug])
    #tags
    tags = TaggableManager()
#Model for comments
class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
    