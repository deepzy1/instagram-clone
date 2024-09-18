from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Post, Comment, Story, Tag,Message,Conversation

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'bio', 'location', 'birth_date', 'profile_picture', 'website')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'bio', 'location', 'birth_date', 'profile_picture', 'website')

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Type your message...'}),
        }

class PostForm(forms.ModelForm):
    tags = forms.CharField(required=False, help_text="Enter tags separated by commas")

    class Meta:
        model = Post
        fields = ['caption', 'image', 'video']
        widgets = {
            'caption': forms.Textarea(attrs={'rows': 3}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            tag_names = [t.strip() for t in self.cleaned_data['tags'].split(',') if t.strip()]
            for tag_name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=tag_name.lower())
                instance.tags.add(tag)
        return instance

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Add a comment...'}),
        }

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['image', 'video', 'caption']
        widgets = {
            'caption': forms.Textarea(attrs={'rows': 2}),
        }

class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)