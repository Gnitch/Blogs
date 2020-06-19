from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User


class Profile(models.Model):
    
    cover = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    status = models.CharField(max_length=500)
    usr = models.ForeignKey('auth.User',on_delete=models.CASCADE,)

class Communities(models.Model) :
    community = models.CharField(max_length=100)

class Blog(models.Model):
    
    title = models.CharField(max_length=200)
    body = models.TextField()
    youtube_video_id = models.CharField(max_length=500)
    video = models.FileField(upload_to='Blogs/Videos',null=True, verbose_name="") 
    usr = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    community = models.ForeignKey(Communities, on_delete=models.SET_NULL, null=True) 
    def get_total_likes(self):
        return self.likes.users.count()

    def get_total_dis_likes(self):
        return self.dis_likes.users.count()

class UploadImages(models.Model):

    cover = models.ImageField(upload_to='Blogs/Images', null=True, blank=True)
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE,)

class BlogComments(models.Model):

    usr = models.ForeignKey('auth.User',on_delete=models.CASCADE,)
    comment = models.TextField(validators=[MinLengthValidator(250)],blank=True)
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE,)

    def __str__(self):
        return str(self.comment)[:30]

class BlogUpvotes(models.Model):
    blog = models.ForeignKey(Blog, related_name="likes", on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='requirement_comment_likes',blank=True)


class BlogDownvotes(models.Model):
    blog = models.ForeignKey(Blog, related_name="dis_likes", on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='requirement_comment_dis_likes',blank=True)    

class BlogSave(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    users = models.ManyToManyField(User, blank=True)    



