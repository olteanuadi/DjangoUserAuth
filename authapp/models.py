from django.db import models
from django.conf import settings
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.contrib.auth.base_user import AbstractBaseUser
# Create your models here.

# class TestUser(AbstractBaseUser):
#     user_name = models.CharField(max_length=50, unique=True)
#     code = models.CharField(max_length=10)

#     USERNAME_FIELD = 'user_name'

#     def __str__(self):
#         return "TestUser object -> {}".format(self.user_name)

class UserRegistrationModel(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    

class User(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # post_id = model
    
# class UserPost(models.Model):
#     user_id = models.ForeignKey(UserRegistrationModel, on_delete=models.CASCADE)
#     post_text = models.CharField(max_length=100)

class FriendRequest(models.Model):
    from_user_id = models.IntegerField(null=True, blank=True)
    user_target_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return "{} sent to {}".format(self.from_user_id, self.user_target_id)

class FriendStatus(models.Model):
    # Getting the main user
    user_id = models.IntegerField()
    # Getting its friend
    friend_id = models.IntegerField()

    def __str__(self):
        return "{} friends with {}".format(self.user_id, self.friend_id)

'''Class for posts
A user can publish a post, with a title and description.
The post will contain the author, the date and time, the number
of likes and the comments from other users.

The person who published the post will be able to see who are
their friends in the comments.'''

class Post(models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField()
    slug = models.SlugField(null=False, unique=True)
    date_and_time = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(UserRegistrationModel, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-date_and_time',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": self.slug})

    # Overriding the 'save' method so the slug is not dependent on the admin page
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        # The save method from the parent
        return super.save(*args, **kwargs)
    


