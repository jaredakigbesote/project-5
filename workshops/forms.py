from django import forms
from .models import Workshop, Session, Review
class WorkshopForm(forms.ModelForm):
    class Meta: model=Workshop; fields=("category","title","short_description","description","base_price","image","is_active")
class SessionForm(forms.ModelForm):
    class Meta: model=Session; fields=("starts_at","ends_at","capacity","location")
class ReviewForm(forms.ModelForm):
    class Meta: model=Review; fields=("rating","comment")
