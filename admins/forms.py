from django import forms

from users.forms import UserRegisterForm, UserProfileForm
from users.models import User
from mainapp.models import CategoryProduct


class UserAdminRegisterForm(UserRegisterForm):

    image = forms.ImageField(widget=forms.FileInput(), required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'image')

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'image':
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-control py-4'


class UserAdminProfileForm(UserProfileForm):

    def __init__(self, *args, **kwargs):
        super(UserAdminProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = False
        self.fields['email'].widget.attrs['readonly'] = False


class CategoryAdminRegisterForm(forms.ModelForm):
    class Meta:
        model = CategoryProduct
        fields = ('name', 'description')

    def __init__(self,*args, **kwargs):
        super(CategoryAdminRegisterForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Введите наименование категории'
        self.fields['description'].widget.attrs['placeholder'] = 'Введите описание категории'
        for field_name, field in self.fields.items():
            if field_name == 'image':
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-control py-4'


class CategoryAdminProfileForm(forms.ModelForm):
    class Meta:
        model = CategoryProduct
        fields = ('name', 'description')

    def __init__(self,*args, **kwargs):
        super(CategoryAdminProfileForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Введите наименование категории'
        self.fields['description'].widget.attrs['placeholder'] = 'Введите описание категории'
        for field_name, field in self.fields.items():
            if field_name == 'image':
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-control py-4'