from django.shortcuts import redirect, render, get_list_or_404, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage

from .models import Profile, UploadImages, Blog
from .forms import ProfileForm, UploadImagesForm, BlogForm

@login_required
def home(request):
    return render(request,'blogs/home.html')

@login_required
def newBlog(request):
    if request.method == 'POST' :
        form1 = BlogForm(request.POST, request.FILES)
        form2 = UploadImagesForm(request.POST,request.FILES)
        if form1.is_valid() or form2.is_valid() :
            youtube_video_id = form1.cleaned_data.get('youtube_video_id')
            if youtube_video_id is not None :
                form1_obj = form1.save(commit=False)            
                form1_obj.youtube_video_id =  getYoutubeId(youtube_video_id)
                form1_obj.usr_id = request.user.id
                blog_obj = form1.save()

            # For form 2
            id_user = request.user.id
            for field in request.FILES.keys():
                for formfile in request.FILES.getlist(field):
                    img_obj = UploadImages(cover=formfile,blog_id=blog_obj.pk)
                    img_obj.save()
                # Redirect to this particular blog
                return redirect('/blogs/')
    
    form1 = BlogForm()
    form2 = UploadImagesForm()
    context = {'form1':form1,'form2':form2}
    return render(request,'blogs/NewBlog.html',context)

def getYoutubeId(link):
    link = link[::-1]
    s = ''
    for each in link :
        if each == '=' :
            break
        else :
            s = s + each       
        
    return s[::-1] 

@login_required
def blogPost(request, blog_pk):
    profile_obj = get_object_or_404(Profile,usr_id=request.user.id)
    blog_obj = get_object_or_404(Blog,pk=blog_pk)
    uploaded_images_lst = list(UploadImages.objects.filter(blog_id=blog_pk))
    first_image = None
    rem_images = None
    if len(uploaded_images_lst) > 0 :
        first_image = uploaded_images_lst[0]
        if len(uploaded_images_lst) > 1 :
            rem_images = uploaded_images_lst[1:]

    context = {'blog_obj':blog_obj,'first_image':first_image,'rem_images':rem_images,'user':request.user,'profile_obj':profile_obj}
    return render(request,'blogs/BlogPost.html',context)


@login_required
def logout(request):
    if request.user.is_authenticated :
        django_logout(request)
    return redirect('/')

@login_required
def Editprofile(request) :
    if request.method == 'POST' :
        form = ProfileForm(request.POST,request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.usr_id = request.user.id
            form.save()
            return redirect('/blogs/profile/')
    
    
    form = ProfileForm()
    context = {'form':form,'type':'edit'}
    return render(request,'blogs/profile.html', context)
    
@login_required
def profile(request) :
    profile_obj = get_object_or_404(Profile,usr_id=request.user.id)
    context = {'user':request.user,'profile_obj':profile_obj}
    return render(request,'blogs/profile.html', context)


    











