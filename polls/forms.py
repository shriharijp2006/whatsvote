from django import forms
from .models import Poll, Option

class CreatePollForm(forms.Form):
    title = forms.CharField(max_length=200, widget=forms.TextInput(attrs={"class": "input"}))
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 3, "class": "textarea"}))
    options_text = forms.CharField(
        help_text="Enter one option per line (min 2).",
        widget=forms.Textarea(attrs={"rows": 5, "class": "textarea"})
    )

    def clean_options_text(self):
        raw = self.cleaned_data["options_text"]
        options = [line.strip() for line in raw.splitlines() if line.strip()]
        if len(options) < 2:
            raise forms.ValidationError("Please provide at least two options.")
        if len(options) > 10:
            raise forms.ValidationError("Limit to 10 options for this demo.")
        return options
