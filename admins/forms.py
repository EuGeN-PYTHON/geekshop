from django import forms

from users.forms import UserRegisterForm, UserProfileForm
from users.models import User
from mainapp.models import CategoryProduct, Product


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
    discount = forms.IntegerField(widget=forms.NumberInput(), label='скидка', required=False, min_value=0, max_value=99,
                                  initial=0)

    class Meta:
        model = CategoryProduct
        fields = ('name', 'description', 'discount')

    def __init__(self, *args, **kwargs):
        super(CategoryAdminRegisterForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Введите наименование категории'
        self.fields['description'].widget.attrs['placeholder'] = 'Введите описание категории'
        self.fields['discount'].widget.attrs['placeholder'] = 'Введите размер скидки'
        for field_name, field in self.fields.items():
            if field_name == 'image':
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-control py-4'


class CategoryAdminProfileForm(forms.ModelForm):
    discount = forms.IntegerField(widget=forms.NumberInput(), label='скидка', required=False, min_value=0, max_value=99,
                                  initial=0)

    class Meta:
        model = CategoryProduct
        fields = ('name', 'description', 'discount')

    def __init__(self,*args, **kwargs):
        super(CategoryAdminProfileForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Введите наименование категории'
        self.fields['description'].widget.attrs['placeholder'] = 'Введите описание категории'
        self.fields['discount'].widget.attrs['placeholder'] = 'Введите размер скидки'
        for field_name, field in self.fields.items():
            if field_name == 'image':
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-control py-4'


class ProductAdminRegisterForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'image', 'quantity', 'category')

    def __init__(self,*args, **kwargs):
        super(ProductAdminRegisterForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Введите наименование категории'
        self.fields['description'].widget.attrs['placeholder'] = 'Введите описание категории'
        self.fields['price'].widget.attrs['placeholder'] = 'Введите цену'
        self.fields['quantity'].widget.attrs['placeholder'] = 'Введите количество'
        self.fields['category'].widget.attrs['placeholder'] = 'Введите категорию'
        for field_name, field in self.fields.items():
            if field_name == 'image':
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-control py-4'


class ProductAdminProfileForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'image', 'quantity', 'category')

    def __init__(self, *args, **kwargs):
        super(ProductAdminProfileForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Введите наименование категории'
        self.fields['description'].widget.attrs['placeholder'] = 'Введите описание категории'
        self.fields['price'].widget.attrs['placeholder'] = 'Введите цену'
        self.fields['quantity'].widget.attrs['placeholder'] = 'Введите количество'
        self.fields['category'].widget.attrs['placeholder'] = 'Введите категорию'
        for field_name, field in self.fields.items():
            if field_name == 'image':
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-control py-4'