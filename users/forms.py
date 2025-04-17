from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from users.models import User

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'input',
        'placeholder': 'Введите эл.почту'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'input',
        'placeholder': 'Введите пароль'

    }))
    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'input',
        'placeholder': 'Введите эл.почту'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'input',
        'placeholder': 'Введите пароль'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'input',
        'placeholder': 'Подтвердите пароль'
    }))

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с такой почтой уже существует')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  # Используем email как username
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    full_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'input',
        'placeholder': 'Введите ФИО'
    }))
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={
        'class': 'input',
        'type': 'date'
    }))
    phone_number = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'input',
        'placeholder': '+7 XXX XXX XX XX'
    }))
    gender = forms.ChoiceField(required=False, choices=[('M', 'Мужской'), ('F', 'Женский')], widget=forms.Select(attrs={
        'class': 'input'
    }))
    technology_stack = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'input',
        'placeholder': 'Введите технологии через запятую'
    }))
    profile_photo = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        'class': 'input'
    }))
    group = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'input',
        'placeholder': 'XXXX-XX-XX'
    }))
    course = forms.ChoiceField(required=False,
        choices=[(None, '-----')] + [(1, '1 курс'), (2, '2 курс'), (3, '3 курс'), (4, '4 курс')],
        widget=forms.Select(attrs={'class': 'input'})
    )
    student_number = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'input',
        'placeholder': 'Личный номер студента'
    }))

    class Meta:
        model = User
        fields = ('full_name', 'date_of_birth', 'phone_number', 'gender', 
                 'technology_stack', 'profile_photo', 'group', 'course', 'student_number')