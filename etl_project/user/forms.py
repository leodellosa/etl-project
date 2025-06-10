from django import forms

class RegistrationForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:ring-red-500 focus:border-red-500 dark:bg-gray-700 dark:text-white'
    }))
    mobile = forms.CharField(widget=forms.TextInput(attrs={
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

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-red-500',
            'placeholder': 'Enter your username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-red-500',
            'placeholder': 'Enter your password'
        })
    )

class ProfileEditForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'mt-1 block w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm'
    }))
    mobile = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'mt-1 block w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm'
    }))
    firstName = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'mt-1 block w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm'
    }))
    middleName = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'mt-1 block w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm'
    }))
    lastName = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'mt-1 block w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm'
    }))
    role = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'mt-1 block w-full rounded-md border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm'
    }))
