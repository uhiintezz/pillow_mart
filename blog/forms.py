from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['created_at', 'post']
        widgets = {
            'name': forms.TextInput(attrs={'class':"form-control", 'name':"name", 'id':"name", 'type':"text", 'placeholder':"Name"}),
            'email': forms.EmailInput(attrs={'class':"form-control", 'name':"email", 'id':"email", 'type':"email", 'placeholder': "Email"}),
            'website': forms.URLInput(attrs={'class':"form-control", 'name':"website", 'id':"website", 'type':"text", 'placeholder': "Website"}),
            'write_comment': forms.Textarea(attrs={'class': "form-control w-100", 'name': "comment", 'id': "comment", 'cols': "30", 'rows': "9", 'placeholder': "Write Comment"})
        }

