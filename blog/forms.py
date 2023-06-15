from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from .models import MyUser, Student, BookDetail, BookingOrder


class StudentCreate(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'course', 'address', 'mobile_number', 'identification_number']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'course': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control'}),
            'identification_number': forms.TextInput(attrs={'class': 'form-control'}),
        }


class BookCreate(forms.ModelForm):
    class Meta:
        model = BookDetail
        fields = ['title', 'author', 'publisher', 'pages', 'price', 'quantity']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'publisher': forms.TextInput(attrs={'class': 'form-control'}),
            'pages': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class UserLoginForms(AuthenticationForm):
    class Meta:
        model = MyUser
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }


class OrderCreate(forms.ModelForm):
    class Meta:
        model = BookingOrder
        fields = ['student', 'book_detail', 'booking_date', 'from_date', 'to_date', 'rent_per_day', 'days', 'amount',
                  'request']
        student = forms.ModelChoiceField(queryset=Student.objects.all()),
        book_detail = forms.ModelChoiceField(queryset=BookDetail.objects.all()),
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'book_detail': forms.Select(attrs={'class': 'form-control'}),
            'booking_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'from_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'to_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'rent_per_day': forms.NumberInput(attrs={'class': 'form-control'}),
            'days': forms.NumberInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'request': forms.BooleanField(initial=False)
        }


class UserSignupForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = MyUser
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

# class BorrowBookForm(forms.ModelForm):
#     class Meta:
#         model = BorrowBook
#         fields = "__all__"
#
#
# class FineCollectForm(forms.ModelForm):
#     class Meta:
#         model = FineCollect
#         fields = "__all__"
