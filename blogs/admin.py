from django.contrib import admin

from .models import Profile, UploadImages, Blog, BlogComments, Communities,BlogDownvotes, BlogUpvotes, BlogSave

admin.site.register(Profile)
admin.site.register(UploadImages)
admin.site.register(Blog)
admin.site.register(BlogComments)
admin.site.register(Communities)
admin.site.register(BlogDownvotes)
admin.site.register(BlogUpvotes)
admin.site.register(BlogSave)






