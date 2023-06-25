from django import forms
from App_Posts.models import Post #calling Post class for their attribute form AppPost project model.py folder

class PostForm(forms.ModelForm):

    class Meta:                     #used to call attributes from Post model with two field image and caption
        model = Post
        fields = ['image','caption']