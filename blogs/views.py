from django.shortcuts import redirect, render, get_list_or_404, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from datetime import date
import os

import SocialWebsite.settings as settings
from .models import Profile, UploadImages, Blog, Communities, BlogComments, BlogUpvotes, BlogDownvotes, BlogSave
from .forms import ProfileForm, UploadImagesForm, BlogForm, UserProfileForm, CommunityForm, BlogCommentsForm


@login_required
def home(request):
    blog_obj = list(Blog.objects.all())
    comm_obj_list = list()
    prof_obj_list = list()
    usr_list = list()
    if len(blog_obj) != 0 :
        for each in blog_obj :
            prof_obj_list.append(get_object_or_404(Profile,usr_id=each.usr_id))
            usr_list.append(get_object_or_404(User,pk=each.usr_id))        
            comm_obj_list.append(get_object_or_404(Communities,pk=each.community_id))

        lst = zip(blog_obj,prof_obj_list,usr_list,comm_obj_list)
        paginator_blog = Paginator(blog_obj,20)
        paginator_prof = Paginator(prof_obj_list,20)
        paginator_usr = Paginator(usr_list,20)
        paginator_comm = Paginator(comm_obj_list,20)

        page_number = request.GET.get('page')
        page_obj1 = paginator_blog.get_page(page_number)  
        page_obj2 = paginator_prof.get_page(page_number)  
        page_obj3 = paginator_usr.get_page(page_number)  
        page_obj4 = paginator_comm.get_page(page_number)  
        
        lst = zip(page_obj1.object_list,page_obj2.object_list,page_obj3.object_list,page_obj4.object_list)        

    else :
        lst = None    
        page_obj1 = None
    context = {'list':lst,'page':'home','page_obj':page_obj1}
    return render(request,'blogs/home.html',context)


@login_required
def myBlogs(request):
    blog_obj = list(Blog.objects.filter(usr_id=request.user.id))
    prof_obj_list = list()
    usr_list = list()
    comm_obj_list = list()
    if blog_obj :
        for each in blog_obj :
            prof_obj_list.append(get_object_or_404(Profile,usr_id=each.usr_id))
            usr_list.append(get_object_or_404(User,pk=request.user.id))        
            comm_obj_list.append(get_object_or_404(Communities,pk=each.community_id))

        lst = zip(blog_obj,prof_obj_list,usr_list,comm_obj_list)
        paginator_blog = Paginator(blog_obj,2)
        paginator_prof = Paginator(prof_obj_list,2)
        paginator_usr = Paginator(usr_list,2)
        paginator_comm = Paginator(comm_obj_list,2)

        page_number = request.GET.get('page')
        page_obj1 = paginator_blog.get_page(page_number)  
        page_obj2 = paginator_prof.get_page(page_number)  
        page_obj3 = paginator_usr.get_page(page_number)  
        page_obj4 = paginator_comm.get_page(page_number)  

        lst = zip(page_obj1.object_list,page_obj2.object_list,page_obj3.object_list,page_obj4.object_list)
    else :
        lst = None
        page_obj1 = None
    context = {'list':lst,'page':'my','page_obj':page_obj1}    
    return render(request,'blogs/home.html',context)

@login_required
def contact(request):
    return render(request,'blogs/contact.html')

@login_required
def search(request):
    if request.method == 'GET' :
        query = str(request.GET.get('q'))
        blog_obj = list(Blog.objects.filter(title__icontains = query))
        prof_obj_list = list()
        usr_list = list()
        if blog_obj :
            for each in blog_obj :
                prof_obj_list.append(get_object_or_404(Profile,usr_id=each.usr_id))
                usr_list.append(get_object_or_404(User,pk=each.usr_id))        
            
            lst = zip(blog_obj,prof_obj_list,usr_list)
        else :
            lst = None          
    
    context = {'list':lst}   
    return render(request,'blogs/home.html',context)

@login_required
def newBlog(request):
    if request.method == 'POST' :
        val = str(request.POST.get('select'))
        comm_obj = get_object_or_404(Communities,pk=val)
        if val is not None :    
            form1 = BlogForm(request.POST, request.FILES)
            form2 = UploadImagesForm(request.POST,request.FILES)
            if form1.is_valid() or form2.is_valid() :
                youtube_video_id = form1.cleaned_data.get('youtube_video_id')
                if youtube_video_id is not None :
                    form1_obj = form1.save(commit=False)   
                    form1_obj.community_id = comm_obj.id     
                    form1_obj.youtube_video_id =  getYoutubeId(youtube_video_id)
                    form1_obj.usr_id = request.user.id
                    blog_obj = form1.save()

                blog_upvote_obj = BlogUpvotes.objects.create(blog_id=blog_obj.id)
                blog_upvote_obj.save()
                blog_save_obj = BlogSave.objects.create(blog_id=blog_obj.id)
                blog_save_obj.save()
                blog_downvote_obj = BlogDownvotes.objects.create(blog_id=blog_obj.id)
                blog_downvote_obj.save()                

                if 'cover' in request.FILES.keys() :
                    id_user = request.user.id
                    for field in request.FILES.keys():
                        if field == 'cover' :
                            print("YES")
                            for formfile in request.FILES.getlist(field):
                                img_obj = UploadImages(cover=formfile,blog_id=blog_obj.pk)
                                img_obj.save()
                    # Redirect to this particular blog
                return redirect('blogs:blogPost', blog_pk=blog_obj.id)

                # blogPost(request,blog_obj.id)
    
    form1 = BlogForm()
    form2 = UploadImagesForm()
    community_list = get_list_or_404(Communities)
    context = {'form1':form1,'form2':form2,'community_list':community_list}
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
    if request.method == 'POST':
        form = BlogCommentsForm(request.POST)
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.usr_id = request.user.id
            form_obj.blog_id = blog_pk
            form_obj.save()

    blog_obj = get_object_or_404(Blog,pk=blog_pk)
    if BlogComments.objects.filter(blog_id=blog_pk).exists():
        comments = get_list_or_404(BlogComments,blog_id=blog_obj.id)
    else :
        comments = []
    user_lst = list()
    for each in comments :
        user_lst.append(get_object_or_404(User,pk=each.usr_id))
    comments_lst = zip(comments,user_lst)
    
    comm_obj = get_object_or_404(Communities,pk=blog_obj.community_id)
    profile_obj = get_object_or_404(Profile,usr_id=blog_obj.usr_id)
    user = get_object_or_404(User,pk=blog_obj.usr_id)
    up_obj = get_object_or_404(BlogUpvotes,blog_id = blog_pk)
    down_obj = get_object_or_404(BlogDownvotes,blog_id = blog_pk)
    uploaded_images_lst = list(UploadImages.objects.filter(blog_id=blog_pk))
    first_image = None
    rem_images = None
    if len(uploaded_images_lst) > 0 :
        first_image = uploaded_images_lst[0]
        if len(uploaded_images_lst) > 1 :
            rem_images = uploaded_images_lst[1:]

    if int(blog_obj.usr_id) == int(request.user.id) :
        owner = 'yes'
    else :
        owner = 'no'

    save_obj = get_object_or_404(BlogSave,blog_id=blog_pk)
    if request.user in save_obj.users.all():        
        saved = True
    else :
        saved = False

    up_but = False
    down_but = False
    if request.user in up_obj.users.all():
        up_but = True

    if request.user in down_obj.users.all():
        down_but = True

    form = BlogCommentsForm()
    context = {'comments_lst':comments_lst,'form':form,'down_but':down_but,'up_but':up_but,
        'saved':saved,'up':up_obj.users.count(),'down':down_obj.users.count(),
        'comm_obj':comm_obj,'owner':owner,'blog_obj':blog_obj,'first_image':first_image,
        'rem_images':rem_images,'user':user,'profile_obj':profile_obj,
    }
    
    return render(request,'blogs/BlogPost.html',context)

@login_required
def deleteBlog(request,blog_pk):
    blog_obj_temp = get_object_or_404(Blog,pk=blog_pk)
    if int(blog_obj_temp.usr_id) == int(request.user.id) :
        if blog_obj_temp.usr_id == request.user.id :
            Blog.objects.filter(pk=blog_pk).delete()
            if UploadImages.objects.filter(blog_id=blog_pk).exists() :
                img_list = list(UploadImages.objects.filter(blog_id=blog_pk))
                for each in img_list :
                    os.remove(os.path.join(settings.MEDIA_ROOT,str(each.cover.name)))
                UploadImages.objects.filter(blog_id=blog_pk).delete()
    return redirect('blogs:home')
 
@login_required
def logout(request):
    if request.user.is_authenticated :
        django_logout(request)
    return redirect('/')

@login_required
def Editprofile(request, user_id) :
    if int(request.user.id) == int(user_id) :
        if request.method == 'POST' :
            form1 = ProfileForm(request.POST,request.FILES)
            form2 = UserProfileForm(request.POST)
            if form1.is_valid() or form2.is_valid():
                if Profile.objects.filter(usr_id = request.user.id).exists() :
                    prof_obj = Profile.objects.get(usr_id = request.user.id)
                    if prof_obj.cover :
                        os.remove(os.path.join(settings.MEDIA_ROOT,str(prof_obj.cover.name)))
                    prof_obj.delete()

                if form2.data['username'] : 
                    username = form2.data['username']
                    user = User.objects.get(pk = request.user.id)
                    user.username = username
                    user.save()
                
                obj = form1.save(commit=False)
                obj.usr_id = request.user.id
                form1.save()
                return redirect('/blogs/profile/')
    
    form1 = ProfileForm()
    form2 = UserProfileForm()
    context = {'form1':form1,'form2':form2,'type':'edit'}
    return render(request,'blogs/profile.html', context)
    
@login_required
def profile(request) :
    profile_obj = get_object_or_404(Profile,usr_id=request.user.id)
    context = {'user':request.user,'profile_obj':profile_obj,'edit':True}
    return render(request,'blogs/profile.html', context)

@login_required
def viewUser(request,usr_id) :
    profile_obj = get_object_or_404(Profile,usr_id=usr_id)
    user = get_object_or_404(User,pk=usr_id)
    if int(usr_id) == int(request.user.id) :
        edit = True
    else :
        edit = False
    

    context = {'user':user,'profile_obj':profile_obj,'edit':edit}
    return render(request,'blogs/profile.html',context)


@login_required
def communityList(request) :   
    community_list = get_list_or_404(Communities)
    context = {'community_list':community_list}
    return render(request,'blogs/communities.html',context)

@login_required
def communityPosts(request,community_id):
    blog_obj = list(Blog.objects.filter(community=community_id))
    comm_obj_list = list()
    prof_obj_list = list()
    usr_list = list()
    if len(blog_obj) != 0 :
        for each in blog_obj :
            prof_obj_list.append(get_object_or_404(Profile,usr_id=each.usr_id))
            usr_list.append(get_object_or_404(User,pk=each.usr_id))        
            comm_obj_list.append(get_object_or_404(Communities,pk=each.community_id))

        lst = zip(blog_obj,prof_obj_list,usr_list,comm_obj_list)

        paginator_blog = Paginator(blog_obj,20)
        paginator_prof = Paginator(prof_obj_list,20)
        paginator_usr = Paginator(usr_list,20)
        paginator_comm = Paginator(comm_obj_list,20)

        page_number = request.GET.get('page')
        page_obj1 = paginator_blog.get_page(page_number)  
        page_obj2 = paginator_prof.get_page(page_number)  
        page_obj3 = paginator_usr.get_page(page_number)  
        page_obj4 = paginator_comm.get_page(page_number)  
        
        lst = zip(page_obj1.object_list,page_obj2.object_list,page_obj3.object_list,page_obj4.object_list)

    else :
        lst = None  
        page_obj1 = None  
        
    context = {'list':lst,'community_id':community_id,'comm':True,'page_obj1':page_obj1}
    return render(request,'blogs/home.html',context)

@login_required
def searchCommunity(request) :
    query = str(request.GET.get('q'))
    if query is not None :
        community_list = list(Communities.objects.filter(community__icontains = query))
    else :
        community_list = get_list_or_404(Communities)
    
    context = {'community_list':community_list}

    if request.is_ajax() :
        html = render_to_string(
            template_name = 'blogs/communitylist.html',
            context = {'community_list':community_list},
        )
        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    return render(request, "blogs/communities.html",context)

@login_required
def communityForm(request):
    if request.method == 'POST' :
        form = CommunityForm(request.POST)
        if form.is_valid() :
            form.save()
            community_list = get_list_or_404(Communities)
            context = {'community_list':community_list}
            return render(request,'blogs/communities.html',context)            

    create = True
    form = CommunityForm()
    context = {'form':form,'create':create}
    return render(request,'blogs/communities.html',context)

@login_required
def upVote(request,blog_pk):
    if  request.is_ajax :
        up_obj = get_object_or_404(BlogUpvotes,blog_id = blog_pk)
        down_obj = get_object_or_404(BlogDownvotes,blog_id = blog_pk)
        if request.user in up_obj.users.all() :
            up_obj.users.remove(request.user)    
        else :
            up_obj.users.add(request.user)
            if request.user in down_obj.users.all() :
                down_obj.users.remove(request.user)    
        print("Yes")
        s = str(up_obj.users.count())+'A'+str(down_obj.users.count())
        return HttpResponse(s)

    blog_obj = get_object_or_404(Blog,pk=blog_pk)
    comm_obj = get_object_or_404(Communities,pk=blog_obj.community_id)
    profile_obj = get_object_or_404(Profile,usr_id=blog_obj.usr_id)
    user = get_object_or_404(User,pk=blog_obj.usr_id)
    uploaded_images_lst = list(UploadImages.objects.filter(blog_id=blog_pk))
    first_image = None
    rem_images = None
    if len(uploaded_images_lst) > 0 :
        first_image = uploaded_images_lst[0]
        if len(uploaded_images_lst) > 1 :
            rem_images = uploaded_images_lst[1:]

    if int(blog_obj.usr_id) == int(request.user.id) :
        owner = 'yes'
    else :
        owner = 'no'

    context = {'comm_obj':comm_obj,'owner':owner,'blog_obj':blog_obj,'first_image':first_image,'rem_images':rem_images,'user':user,'profile_obj':profile_obj}
    return render(request,'blogs/BlogPost.html',context)

    
@login_required
def downVote(request,blog_pk):
    if  request.is_ajax :
        up_obj = get_object_or_404(BlogUpvotes,blog_id = blog_pk)
        down_obj = get_object_or_404(BlogDownvotes,blog_id = blog_pk)
        if request.user in down_obj.users.all() :
            down_obj.users.remove(request.user)    
        else :
            down_obj.users.add(request.user)
            if request.user in down_obj.users.all() :
                up_obj.users.remove(request.user)    

        s = str(up_obj.users.count())+'A'+str(down_obj.users.count())
        return HttpResponse(s)

    blog_obj = get_object_or_404(Blog,pk=blog_pk)
    comm_obj = get_object_or_404(Communities,pk=blog_obj.community_id)
    profile_obj = get_object_or_404(Profile,usr_id=blog_obj.usr_id)
    user = get_object_or_404(User,pk=blog_obj.usr_id)
    uploaded_images_lst = list(UploadImages.objects.filter(blog_id=blog_pk))
    first_image = None
    rem_images = None
    if len(uploaded_images_lst) > 0 :
        first_image = uploaded_images_lst[0]
        if len(uploaded_images_lst) > 1 :
            rem_images = uploaded_images_lst[1:]

    if int(blog_obj.usr_id) == int(request.user.id) :
        owner = 'yes'
    else :
        owner = 'no'

    context = {'comm_obj':comm_obj,'owner':owner,'blog_obj':blog_obj,'first_image':first_image,'rem_images':rem_images,'user':user,'profile_obj':profile_obj}
    return render(request,'blogs/BlogPost.html',context)

def saved(request,blog_pk) :
    if request.is_ajax :
        save_obj = get_object_or_404(BlogSave,blog_id=blog_pk)
        if request.user not in save_obj.users.all() :
            save_obj.users.add(request.user)
            print(save_obj.users.count())
            return HttpResponse('Saved')

        else :
            save_obj.users.remove(request.user)
            print(save_obj.users.count())
            return HttpResponse('Removed from saved')

    blog_obj = get_object_or_404(Blog,pk=blog_pk)
    comm_obj = get_object_or_404(Communities,pk=blog_obj.community_id)
    profile_obj = get_object_or_404(Profile,usr_id=blog_obj.usr_id)
    user = get_object_or_404(User,pk=blog_obj.usr_id)
    uploaded_images_lst = list(UploadImages.objects.filter(blog_id=blog_pk))
    first_image = None
    rem_images = None
    if len(uploaded_images_lst) > 0 :
        first_image = uploaded_images_lst[0]
        if len(uploaded_images_lst) > 1 :
            rem_images = uploaded_images_lst[1:]

    if int(blog_obj.usr_id) == int(request.user.id) :
        owner = 'yes'
    else :
        owner = 'no'

    context = {'comm_obj':comm_obj,'owner':owner,'blog_obj':blog_obj,'first_image':first_image,'rem_images':rem_images,'user':user,'profile_obj':profile_obj}
    return render(request,'blogs/BlogPost.html',context)


@login_required
def sortUpvotes(request, page):
    blog_obj = list() 
    if page == 'my' :
        up_obj_lst = list()
        blog_obj_my = get_list_or_404(Blog,usr_id=request.user.id)
        for each in blog_obj_my :
            up_obj_lst.append(get_object_or_404(BlogUpvotes,blog_id=each.id))

        up_obj_lst.sort(key = lambda x : x.users.count(),reverse=True)
        for each in up_obj_lst :
            blog_obj.append(get_object_or_404(Blog,pk=each.blog_id))
    
    else :

        up_obj_lst = list(get_list_or_404(BlogUpvotes))
        up_obj_lst.sort(key = lambda x : x.users.count(),reverse=True)
        for each in up_obj_lst :
            blog_obj.append(get_object_or_404(Blog,pk=each.blog_id))    
    
    comm_obj_list = list()
    prof_obj_list = list()
    usr_list = list()
    if len(blog_obj) != 0 :
        for each in blog_obj :
            prof_obj_list.append(get_object_or_404(Profile,usr_id=each.usr_id))
            usr_list.append(get_object_or_404(User,pk=each.usr_id))        
            comm_obj_list.append(get_object_or_404(Communities,pk=each.community_id))

        lst = zip(blog_obj,prof_obj_list,usr_list,comm_obj_list)

        paginator_blog = Paginator(blog_obj,20)
        paginator_prof = Paginator(prof_obj_list,20)
        paginator_usr = Paginator(usr_list,20)
        paginator_comm = Paginator(comm_obj_list,20)

        page_number = request.GET.get('page')
        page_obj1 = paginator_blog.get_page(page_number)  
        page_obj2 = paginator_prof.get_page(page_number)  
        page_obj3 = paginator_usr.get_page(page_number)  
        page_obj4 = paginator_comm.get_page(page_number)  
        
        lst = zip(page_obj1.object_list,page_obj2.object_list,page_obj3.object_list,page_obj4.object_list)

    else :
        lst = None    
        page_obj1 = None
    context = {'list':lst,'page_obj':page_obj1}
    return render(request,'blogs/home.html',context)


@login_required
def sortDownvotes(request, page):
    blog_obj = list() 
    if page == 'my' :
        up_obj_lst = list()
        blog_obj_my = get_list_or_404(Blog,usr_id=request.user.id)
        for each in blog_obj_my :
            up_obj_lst.append(get_object_or_404(BlogDownvotes,blog_id=each.id))

        up_obj_lst.sort(key = lambda x : x.users.count(),reverse=True)
        for each in up_obj_lst :
            blog_obj.append(get_object_or_404(Blog,pk=each.blog_id))
    else :

        up_obj_lst = list(get_list_or_404(BlogDownvotes))
        up_obj_lst.sort(key = lambda x : x.users.count(),reverse=True)
        for each in up_obj_lst :
            blog_obj.append(get_object_or_404(Blog,pk=each.blog_id))    

    comm_obj_list = list()
    prof_obj_list = list()
    usr_list = list()
    if len(blog_obj) != 0 :
        for each in blog_obj :
            prof_obj_list.append(get_object_or_404(Profile,usr_id=each.usr_id))
            usr_list.append(get_object_or_404(User,pk=each.usr_id))        
            comm_obj_list.append(get_object_or_404(Communities,pk=each.community_id))

        lst = zip(blog_obj,prof_obj_list,usr_list,comm_obj_list)

        paginator_blog = Paginator(blog_obj,20)
        paginator_prof = Paginator(prof_obj_list,20)
        paginator_usr = Paginator(usr_list,20)
        paginator_comm = Paginator(comm_obj_list,20)

        page_number = request.GET.get('page')
        page_obj1 = paginator_blog.get_page(page_number)  
        page_obj2 = paginator_prof.get_page(page_number)  
        page_obj3 = paginator_usr.get_page(page_number)  
        page_obj4 = paginator_comm.get_page(page_number)  
        
        lst = zip(page_obj1.object_list,page_obj2.object_list,page_obj3.object_list,page_obj4.object_list)

    else :
        lst = None    
        page_obj1 = None
    context = {'list':lst,'page_obj':page_obj1}
    return render(request,'blogs/home.html',context)


@login_required
def savedBlogs(request):
    blog_sav_lst = list(BlogSave.objects.filter(users=request.user))
    blog_obj = list()
    comm_obj_list = list()
    prof_obj_list = list()
    usr_list = list()
    if len(blog_obj) != 0 :
        for each in blog_sav_lst :
            blog_obj.append(get_object_or_404(Blog,pk=each.blog_id))

        for each in blog_obj :
            prof_obj_list.append(get_object_or_404(Profile,usr_id=each.usr_id))
            usr_list.append(get_object_or_404(User,pk=each.usr_id))        
            comm_obj_list.append(get_object_or_404(Communities,pk=each.community_id))

        lst = zip(blog_obj,prof_obj_list,usr_list,comm_obj_list)

        paginator_blog = Paginator(blog_obj,20)
        paginator_prof = Paginator(prof_obj_list,20)
        paginator_usr = Paginator(usr_list,20)
        paginator_comm = Paginator(comm_obj_list,20)

        page_number = request.GET.get('page')
        page_obj1 = paginator_blog.get_page(page_number)  
        page_obj2 = paginator_prof.get_page(page_number)  
        page_obj3 = paginator_usr.get_page(page_number)  
        page_obj4 = paginator_comm.get_page(page_number)  
        
        lst = zip(page_obj1.object_list,page_obj2.object_list,page_obj3.object_list,page_obj4.object_list)

    else :
        lst = None    
        page_obj1 = None
    context = {'list':lst,'page_obj':page_obj1}
    return render(request,'blogs/home.html',context)


@login_required
def sortNew(request, page):
    if page == 'my' :
        blog_obj = list(Blog.objects.filter(usr_id=request.user.id).order_by('date').order_by('date__hour', 'date__minute'))
    else :
        blog_obj = list(Blog.objects.order_by('date').order_by('date__hour', 'date__minute'))

    comm_obj_list = list()
    prof_obj_list = list()
    usr_list = list()
    if len(blog_obj) != 0 :
        for each in blog_obj :
            prof_obj_list.append(get_object_or_404(Profile,usr_id=each.usr_id))
            usr_list.append(get_object_or_404(User,pk=each.usr_id))        
            comm_obj_list.append(get_object_or_404(Communities,pk=each.community_id))

        lst = zip(blog_obj,prof_obj_list,usr_list,comm_obj_list)
        paginator_blog = Paginator(blog_obj,20)
        paginator_prof = Paginator(prof_obj_list,20)
        paginator_usr = Paginator(usr_list,20)
        paginator_comm = Paginator(comm_obj_list,20)

        page_number = request.GET.get('page')
        page_obj1 = paginator_blog.get_page(page_number)  
        page_obj2 = paginator_prof.get_page(page_number)  
        page_obj3 = paginator_usr.get_page(page_number)  
        page_obj4 = paginator_comm.get_page(page_number)  
        
        lst = zip(page_obj1.object_list,page_obj2.object_list,page_obj3.object_list,page_obj4.object_list)

    else :
        lst = None    
        page_obj1 = None
    context = {'list':lst,'page_obj':page_obj1}
    return render(request,'blogs/home.html',context)

@login_required
def sortOld(request, page):
    if page == 'my' :
        blog_obj = list(Blog.objects.filter(usr_id=request.user.id).order_by('-date').order_by('-date__hour', '-date__minute'))
    else :
        blog_obj = list(Blog.objects.order_by('-date').order_by('-date__hour', '-date__minute'))

    comm_obj_list = list()
    prof_obj_list = list()
    usr_list = list()
    if len(blog_obj) != 0 :
        for each in blog_obj :
            prof_obj_list.append(get_object_or_404(Profile,usr_id=each.usr_id))
            usr_list.append(get_object_or_404(User,pk=each.usr_id))        
            comm_obj_list.append(get_object_or_404(Communities,pk=each.community_id))

        lst = zip(blog_obj,prof_obj_list,usr_list,comm_obj_list)

        paginator_blog = Paginator(blog_obj,20)
        paginator_prof = Paginator(prof_obj_list,20)
        paginator_usr = Paginator(usr_list,20)
        paginator_comm = Paginator(comm_obj_list,20)

        page_number = request.GET.get('page')
        page_obj1 = paginator_blog.get_page(page_number)  
        page_obj2 = paginator_prof.get_page(page_number)  
        page_obj3 = paginator_usr.get_page(page_number)  
        page_obj4 = paginator_comm.get_page(page_number)  
        
        lst = zip(page_obj1.object_list,page_obj2.object_list,page_obj3.object_list,page_obj4.object_list)

    else :
        lst = None    
        page_obj1 = None
    context = {'list':lst,'page_obj':page_obj1}
    return render(request,'blogs/home.html',context)

@login_required
def trendingToday(request,page):
    up_obj_lst = list()
    blog_obj = list()
    if page == 'my' :
        blog_obj_my = list(Blog.objects.filter(usr_id=request.user.id).filter(date__date = date.today()))
        if len(blog_obj_my) != 0 :
            for each in blog_obj_my :
                up_obj_lst.append(get_object_or_404(BlogUpvotes,blog_id=each.id))

            up_obj_lst.sort(key = lambda x : x.users.count(),reverse=True)
            for each in up_obj_lst :
                blog_obj.append(get_object_or_404(Blog,pk=each.blog_id))        
        
    else :
        blog_obj_my = list(Blog.objects.filter(date__date = date.today()))
        if len(blog_obj_my) != 0 :
            for each in blog_obj_my :
                up_obj_lst.append(get_object_or_404(BlogUpvotes,blog_id=each.id))

            up_obj_lst.sort(key = lambda x : x.users.count(),reverse=True)
            for each in up_obj_lst :
                blog_obj.append(get_object_or_404(Blog,pk=each.blog_id))   


    comm_obj_list = list()
    prof_obj_list = list()
    usr_list = list()
    if len(blog_obj) != 0 :
        for each in blog_obj :
            prof_obj_list.append(get_object_or_404(Profile,usr_id=each.usr_id))
            usr_list.append(get_object_or_404(User,pk=each.usr_id))        
            comm_obj_list.append(get_object_or_404(Communities,pk=each.community_id))

        lst = zip(blog_obj,prof_obj_list,usr_list,comm_obj_list)

        paginator_blog = Paginator(blog_obj,20)
        paginator_prof = Paginator(prof_obj_list,20)
        paginator_usr = Paginator(usr_list,20)
        paginator_comm = Paginator(comm_obj_list,20)

        page_number = request.GET.get('page')
        page_obj1 = paginator_blog.get_page(page_number)  
        page_obj2 = paginator_prof.get_page(page_number)  
        page_obj3 = paginator_usr.get_page(page_number)  
        page_obj4 = paginator_comm.get_page(page_number)  
        
        lst = zip(page_obj1.object_list,page_obj2.object_list,page_obj3.object_list,page_obj4.object_list)

    else :
        lst = None    
        page_obj1 = None
    context = {'list':lst,'page_obj':page_obj1}
    return render(request,'blogs/home.html',context)    

@login_required
def sortUpvotesComm(request,community_id):
    blog_obj = list(Blog.objects.filter(community=community_id))    
    up_obj_lst = list()
    if len(blog_obj) != 0 :
        for each in blog_obj :
                up_obj_lst.append(get_object_or_404(BlogUpvotes,blog_id=each.id))

        up_obj_lst.sort(key = lambda x : x.users.count(),reverse=True)
        blog_obj = []
        for each in up_obj_lst :
                blog_obj.append(get_object_or_404(Blog,pk=each.blog_id))

        comm_obj_list = list()
        prof_obj_list = list()
        usr_list = list()
    
        for each in blog_obj :
            prof_obj_list.append(get_object_or_404(Profile,usr_id=each.usr_id))
            usr_list.append(get_object_or_404(User,pk=each.usr_id))        
            comm_obj_list.append(get_object_or_404(Communities,pk=each.community_id))

        lst = zip(blog_obj,prof_obj_list,usr_list,comm_obj_list)

        paginator_blog = Paginator(blog_obj,20)
        paginator_prof = Paginator(prof_obj_list,20)
        paginator_usr = Paginator(usr_list,20)
        paginator_comm = Paginator(comm_obj_list,20)

        page_number = request.GET.get('page')
        page_obj1 = paginator_blog.get_page(page_number)  
        page_obj2 = paginator_prof.get_page(page_number)  
        page_obj3 = paginator_usr.get_page(page_number)  
        page_obj4 = paginator_comm.get_page(page_number)  
        
        lst = zip(page_obj1.object_list,page_obj2.object_list,page_obj3.object_list,page_obj4.object_list)
        
    else :
        lst = None    
        page_obj1 = None
    context = {'list':lst,'community_id':community_id,'page_obj':page_obj1}
    return render(request,'blogs/home.html',context)

@login_required
def sortDownvotesComm(request,community_id):
    blog_obj = list(Blog.objects.filter(community=community_id))  
    if len(blog_obj) != 0 :
        up_obj_lst = list()
        for each in blog_obj :
                up_obj_lst.append(get_object_or_404(BlogDownvotes,blog_id=each.id))

        up_obj_lst.sort(key = lambda x : x.users.count(),reverse=True)
        blog_obj = []
        for each in up_obj_lst :
                blog_obj.append(get_object_or_404(Blog,pk=each.blog_id))

        comm_obj_list = list()
        prof_obj_list = list()
        usr_list = list()

        for each in blog_obj :
            prof_obj_list.append(get_object_or_404(Profile,usr_id=each.usr_id))
            usr_list.append(get_object_or_404(User,pk=each.usr_id))        
            comm_obj_list.append(get_object_or_404(Communities,pk=each.community_id))

        lst = zip(blog_obj,prof_obj_list,usr_list,comm_obj_list)

        paginator_blog = Paginator(blog_obj,20)
        paginator_prof = Paginator(prof_obj_list,20)
        paginator_usr = Paginator(usr_list,20)
        paginator_comm = Paginator(comm_obj_list,20)

        page_number = request.GET.get('page')
        page_obj1 = paginator_blog.get_page(page_number)  
        page_obj2 = paginator_prof.get_page(page_number)  
        page_obj3 = paginator_usr.get_page(page_number)  
        page_obj4 = paginator_comm.get_page(page_number)  
        
        lst = zip(page_obj1.object_list,page_obj2.object_list,page_obj3.object_list,page_obj4.object_list)

    else :
        lst = None    
        page_obj1 = None
    context = {'list':lst,'community_id':community_id,'page_obj':page_obj1}
    return render(request,'blogs/home.html',context)


@login_required
def sortNewComm(request,community_id):
    blog_obj = list(Blog.objects.filter(community=community_id).order_by('date').order_by('date__hour', 'date__minute'))    
    comm_obj_list = list()
    prof_obj_list = list()
    usr_list = list()
    if len(blog_obj) != 0 :
        for each in blog_obj :
            prof_obj_list.append(get_object_or_404(Profile,usr_id=each.usr_id))
            usr_list.append(get_object_or_404(User,pk=each.usr_id))        
            comm_obj_list.append(get_object_or_404(Communities,pk=each.community_id))

        lst = zip(blog_obj,prof_obj_list,usr_list,comm_obj_list)

        paginator_blog = Paginator(blog_obj,20)
        paginator_prof = Paginator(prof_obj_list,20)
        paginator_usr = Paginator(usr_list,20)
        paginator_comm = Paginator(comm_obj_list,20)

        page_number = request.GET.get('page')
        page_obj1 = paginator_blog.get_page(page_number)  
        page_obj2 = paginator_prof.get_page(page_number)  
        page_obj3 = paginator_usr.get_page(page_number)  
        page_obj4 = paginator_comm.get_page(page_number)  
        
        lst = zip(page_obj1.object_list,page_obj2.object_list,page_obj3.object_list,page_obj4.object_list)

    else :
        lst = None    
        page_obj1 = None
    context = {'list':lst,'community_id':community_id,'page_obj':page_obj1}
    return render(request,'blogs/home.html',context)

@login_required
def sortOldComm(request,community_id):
    blog_obj = list(Blog.objects.filter(community=community_id).order_by('-date').order_by('-date__hour', '-date__minute'))    
    comm_obj_list = list()
    prof_obj_list = list()
    usr_list = list()
    if len(blog_obj) != 0 :
        for each in blog_obj :
            prof_obj_list.append(get_object_or_404(Profile,usr_id=each.usr_id))
            usr_list.append(get_object_or_404(User,pk=each.usr_id))        
            comm_obj_list.append(get_object_or_404(Communities,pk=each.community_id))

        lst = zip(blog_obj,prof_obj_list,usr_list,comm_obj_list)

        paginator_blog = Paginator(blog_obj,20)
        paginator_prof = Paginator(prof_obj_list,20)
        paginator_usr = Paginator(usr_list,20)
        paginator_comm = Paginator(comm_obj_list,20)

        page_number = request.GET.get('page')
        page_obj1 = paginator_blog.get_page(page_number)  
        page_obj2 = paginator_prof.get_page(page_number)  
        page_obj3 = paginator_usr.get_page(page_number)  
        page_obj4 = paginator_comm.get_page(page_number)  
        
        lst = zip(page_obj1.object_list,page_obj2.object_list,page_obj3.object_list,page_obj4.object_list)

    else :
        lst = None    
        page_obj1 = None
    context = {'list':lst,'community_id':community_id,'page_obj':page_obj1}
    return render(request,'blogs/home.html',context)

@login_required
def trendingTodayComm(request,community_id):
    up_obj_lst = list()
    blog_obj = list()
    blog_obj_my = list(Blog.objects.filter(community=community_id).filter(date__date = date.today()))
    if len(blog_obj_my) != 0 :
        for each in blog_obj_my :
            up_obj_lst.append(get_object_or_404(BlogUpvotes,blog_id=each.id))

        up_obj_lst.sort(key = lambda x : x.users.count(),reverse=True)
        for each in up_obj_lst :
            blog_obj.append(get_object_or_404(Blog,pk=each.blog_id))   

    comm_obj_list = list()
    prof_obj_list = list()
    usr_list = list()
    if len(blog_obj) != 0 :
        for each in blog_obj :
            prof_obj_list.append(get_object_or_404(Profile,usr_id=each.usr_id))
            usr_list.append(get_object_or_404(User,pk=each.usr_id))        
            comm_obj_list.append(get_object_or_404(Communities,pk=each.community_id))

        lst = zip(blog_obj,prof_obj_list,usr_list,comm_obj_list)

        paginator_blog = Paginator(blog_obj,20)
        paginator_prof = Paginator(prof_obj_list,20)
        paginator_usr = Paginator(usr_list,20)
        paginator_comm = Paginator(comm_obj_list,20)

        page_number = request.GET.get('page')
        page_obj1 = paginator_blog.get_page(page_number)  
        page_obj2 = paginator_prof.get_page(page_number)  
        page_obj3 = paginator_usr.get_page(page_number)  
        page_obj4 = paginator_comm.get_page(page_number)  
        
        lst = zip(page_obj1.object_list,page_obj2.object_list,page_obj3.object_list,page_obj4.object_list)

    else :
        lst = None    
        page_obj1 = None
    context = {'list':lst,'community_id':community_id,'page_obj':page_obj1}
    return render(request,'blogs/home.html',context)

@login_required
def deleteComment(request, comment_pk, blog_pk) :
    comment_obj = get_object_or_404(BlogComments,pk = comment_pk)
    if int(comment_obj.usr_id) == int(request.user.id) :
        comment_obj.delete()
    return redirect('blogs:blogPost', blog_pk=blog_pk)
