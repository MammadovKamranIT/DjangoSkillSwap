from django import forms
from.models import Offer

class ContactForm(forms.Form):
    name = forms.CharField(
        label='Имя',
        max_length=100,
        min_length=1,
        widget=forms.TextInput(attrs={'placeholder':'Enter your name'})
    )
    email = forms.EmailField(
        label='Почта',
        widget=forms.EmailInput(attrs={'placeholder':'Enter your email'}))

    message = forms.CharField(
        label="Сообщение",
        widget=forms.Textarea(attrs={'placeholder':'Enter your message', 'rows':'5'}),
    )


class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['title','content', 'category','tags']

        labels = {

            'title': "Title",
            'content': "Content",
            'category': "Category",
            'tag': "Tags",
        }




        widgets = {

        "title": forms.TextInput(),
        'content': forms.Textarea(attrs={'rows':6}),
        'category':forms.Select(), 
        'tags':forms.SelectMultiple()
                                                                                   
        }




 

def clean_title(self):
    title = self.cleaned_data['title'].strip()
    if title.lower().startswith('test'):
        raise forms.ValidationError("Title should not start with 'test'")
    return title