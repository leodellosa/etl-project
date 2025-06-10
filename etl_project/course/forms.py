from django import forms

class CourseForm(forms.Form):
    title = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        'class': 'form-input w-full',
        'placeholder': 'Enter course title'
    }))
    description = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-textarea w-full',
        'placeholder': 'Enter course description',
        'rows': 3
    }))

class LevelForm(forms.Form):
    LEVEL_CHOICES = [
        ('BEGINNER', 'BEGINNER'),
        ('INTERMEDIATE', 'INTERMEDIATE'),
        ('ADVANCE', 'ADVANCE'),
    ]
    name = forms.ChoiceField(
        choices=LEVEL_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select w-full',
            'placeholder': 'Select level'
        })
    )

class CategoryForm(forms.Form):
    CATEGORY_CHOICES = [
        ('EXERCISE', 'EXERCISE'),
        ('REFERENCE', 'REFERENCE')
    ]
    name = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select w-full',
            'placeholder': 'Category name'
        })
    )

class ItemForm(forms.Form):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        'class': 'form-input w-full',
        'placeholder': 'Item description'
    }))

