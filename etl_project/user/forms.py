from django import forms

class RegistrationForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-red-500 focus:border-red-500 dark:bg-gray-700 dark:text-white'
    }))
    mobile = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-red-500 focus:border-red-500 dark:bg-gray-700 dark:text-white'
    }))
    firstName = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm dark:bg-gray-700 dark:text-white'
    }))
    middleName = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm dark:bg-gray-700 dark:text-white'
    }))
    lastName = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm dark:bg-gray-700 dark:text-white'
    }))
    role = forms.ChoiceField(choices=[
        ('admin', 'Admin'),
        ('instructor', 'Instructor'),
        ('learner', 'Learner'),
    ], widget=forms.Select(attrs={
        'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm dark:bg-gray-700 dark:text-white'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm dark:bg-gray-700 dark:text-white'
    }))
    plain_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm dark:bg-gray-700 dark:text-white'
    }))
