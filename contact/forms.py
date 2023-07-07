from django import forms
from .models import AboutSubscription


from .models import ContactModel, About

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactModel
        exclude = ['created_at']
        widgets = {
            'name': forms.TextInput(attrs={'class':"form-control", 'name':"name", 'id':"name", 'type':"text", 'onfocus':
            "this.placeholder = ''",
                    'onblur': "this.placeholder = 'Enter your name'", 'placeholder':'Enter your name'}),

            'email': forms.EmailInput(attrs={'class':"form-control", 'name':"email", 'id':"email", 'type':"email", 'onfocus':"this.placeholder = ''",
                    'onblur':"this.placeholder = 'Enter email address'", 'placeholder':'Enter email address'}),

            'website': forms.URLInput(attrs={'class':"form-control", 'name':"website", 'id':"subject", 'type':"text" ,'onfocus':"this.placeholder = ''",
                    'onblur':"this.placeholder = 'Enter Website'", 'placeholder':'Enter Website'}),

            'message': forms.Textarea(attrs={'class':"form-control w-100", 'name':"message", 'id':"message", 'cols':"30", 'rows':"9",
                    'onfocus':"this.placeholder = ''", 'onblur':"this.placeholder = 'Enter Message'",
                    'placeholder':'Enter Message'})
}


class AboutSubscriptionForm(forms.ModelForm):

    class Meta:
        model = AboutSubscription
        fields = ['email']

        widgets = {
            'email': forms.TextInput(attrs={'type':"text", 'placeholder':"Enter your mail", 'id':"my-input", 'class':'my-input'})
        }
