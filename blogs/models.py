from django.db import models

class Profile(models.Model):
    
    cover = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    status = models.CharField(max_length=500)
    usr = models.ForeignKey('auth.User',on_delete=models.CASCADE,)

    def delete(self, *args, **kwargs):
        self.cover.delete()
        super().delete(*args, **kwargs)

class Blog(models.Model):
    
    title = models.CharField(max_length=200)
    body = models.TextField()
    youtube_video_id = models.CharField(max_length=500)
    video = models.FileField(upload_to='Blogs/Videos',null=True, verbose_name="") 
    usr = models.ForeignKey('auth.User',on_delete=models.CASCADE,)

class UploadImages(models.Model):

    cover = models.ImageField(upload_to='Blogs/Images', null=True, blank=True)
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE)





