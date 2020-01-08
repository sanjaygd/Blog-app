from django.db import models
from django.conf import settings
from django.urls import reverse
# from django.shortcuts import reverse
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.text import slugify



class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())

def upload_location(instance, filename):
    return '%s/%s' %(instance.id, filename)

class Post(models.Model):
    title = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    draft = models.BooleanField(default=False)
    publish = models.DateTimeField(auto_now=False, auto_now_add=False)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=upload_location,
            null=True,
            blank=True, 
            width_field="width_field", 
            height_field="hieght_field")
    hieght_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField()
    updates = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = PostManager()

    def __str__(self):
        return self.title

    

    # def get_absolute_url(self):
    #     return reverse('post:detail', kwargs={'pk':self.id})
    #     # return 'detail/{}'.format(self.id)
    # # Add this part in url to get detail page   <a href="{% url 'post:detail' pk=obj.id %}"> {{obj.title}} </a>

    def get_absolute_url(self):
        return reverse('post:detail', kwargs={'slug':self.slug})

    class Meta:
        ordering = ["-timestamp", "-updates"]



def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = '%s-%s' %(slug,qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug



def pre_save_post_reciever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_reciever, sender=Post)

    