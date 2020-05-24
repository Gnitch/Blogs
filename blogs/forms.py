from django import forms

from .models import Profile, Blog, UploadImages

class ProfileForm(forms.ModelForm) :
    
    class Meta:
        model = Profile
        fields = ('status','cover',)
        widgets = {
            'status': forms.TextInput(attrs={'class': 'form-custom','placeholder':'Enter Status  Eg. WEEB'}),
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
        fields = ('title','body','youtube_video_id','video')
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
        self.fields['video'].help_text = " video should be in .mp4 "
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


