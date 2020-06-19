from django import forms
from django.contrib.auth.models import User

from .models import Profile, Blog, UploadImages, Communities

class CommunityForm(forms.ModelForm):
    class Meta :
        model = Communities
        fields = ('community',)
        widgets = {
            'community': forms.TextInput(attrs={'class': 'form-custom','placeholder':'Enter Community name'}),
        }        
        labels ={
            'community' : (''),            
        }        
    def __init__(self, *args, **kwargs):
        super(CommunityForm, self).__init__(*args, **kwargs)        
        self.fields['community'].required = False        

class UserProfileForm(forms.ModelForm):
    class Meta :
        model = User
        fields = ('username',)
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-custom','placeholder':'Enter Username'}),
        }        
        labels = {
            'username' : (''),
        }    
        help_texts = {
            'username': None,
        } 
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)        
        self.fields['username'].required = False

class ProfileForm(forms.ModelForm) :
    
    class Meta:
        model = Profile
        fields = ('status','cover',)
        widgets = {
            'status': forms.TextInput(attrs={'class': 'form-custom','placeholder':'Enter Status  Eg. WEEB or DEVELOPER or CHEF'}),
        }
        labels = {
            'status' : (''),
            'cover' : (''),
        }   
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['status'].required=False
        self.fields['cover'].required=False

class BlogForm(forms.ModelForm):
    
    class Meta:
        model = Blog
        fields = ('title','body','youtube_video_id','video',)
        widgets = {
            'title':forms.TextInput(attrs={'class': 'form-custom','placeholder':'Enter Title'}),
            'body':forms.Textarea(attrs={'class': 'form-custom body','placeholder':'Enter Body'}),
            'youtube_video_id':forms.TextInput(attrs={'class': 'form-custom','placeholder':'Enter Youtube link'})
        }
        labels ={
            'title' : (''),
            'body' : (''),
            'youtube_video_id' : (''),
            'video' : ('Upload Video:'),
        }
    def __init__(self, *args, **kwargs):
        super(BlogForm, self).__init__(*args, **kwargs)
        self.fields['video'].help_text = " Video should be in .mp4 format"
        self.fields['title'].required=True 
        self.fields['body'].required=False
        self.fields['youtube_video_id'].required=False
        self.fields['video'].required=False

class UploadImagesForm(forms.ModelForm):
    
    class Meta :
        model = UploadImages 
        fields = ('cover',) 
        widgets= {
            'cover':forms.ClearableFileInput(attrs={'multiple':True}),
        }
        labels = {
            'cover' : ('Upload Images:'),
        }

    def __init__(self, *args, **kwargs):
        super(UploadImagesForm, self).__init__(*args, **kwargs)
        self.fields['cover'].required=False

# class BlogCommentsForm(forms.ModelForm) :

#     class Meta :
#         model = BlogComments
#         fields = ('comments',)
#         widgets = {
#             'comments':forms.TextInput(attrs={'class': 'form-comments','placeholder':'Enter Text'})
#         }
#         labels = {
#             'comments' : (''),
#         }
#     def __init__(self, *args, **kwargs):
#         super(BlogCommentsForm, self).__init__(*args, **kwargs)
#         self.fields['comments'].required=True 



























