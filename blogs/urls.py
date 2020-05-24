from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name='blogs'
urlpatterns = [
    path('logout/',views.logout ,name='logout'),
    path('',views.home ,name='home'),
    path('profile/',views.profile ,name='profile'),
    path('new_blog/',views.newBlog ,name='newBlog'),
    path('blog_post/<int:blog_pk>',views.blogPost ,name='blogPost'),
    path('edit_profile/',views.Editprofile ,name='Editprofile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



