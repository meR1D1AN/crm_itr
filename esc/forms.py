from django import forms

from problems.models import Problem
from replacements.models import Replacement


class EscProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ["problem"]


class EscReplacementeForm(forms.ModelForm):
    class Meta:
        model = Replacement
        fields = ["info_replacement"]
