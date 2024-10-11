from django import forms
from django.core.exceptions import ValidationError
from store.models import ProductReview

class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['title', 'review_text', 'rating']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control my-2', 'placeholder': 'Enter review title'}),
            'review_text': forms.Textarea(attrs={'class': 'form-control my-2', 'placeholder': 'Write your review'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control my-2', 'min': '1', 'max': '5'}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise ValidationError("The title must be at least 5 characters long.")
        if len(title) > 200:
            raise ValidationError("The title cannot be more than 200 characters long.")
        return title

    def clean_review_text(self):
        review_text = self.cleaned_data.get('review_text')
        if len(review_text) < 20:
            raise ValidationError("The review must be at least 20 characters long.")
        if len(review_text) > 2000:
            raise ValidationError("The review cannot be more than 2000 characters long.")
        return review_text

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating is None:
            raise ValidationError("Please provide a rating.")
        if rating < 1 or rating > 5:
            raise ValidationError("Rating must be between 1 and 5.")
        return rating

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        review_text = cleaned_data.get('review_text')

        if title and review_text:
            if title.lower() in review_text.lower():
                raise ValidationError("The review text should not contain the title.")

        return cleaned_data