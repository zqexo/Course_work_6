from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError

from main.models import Client


class StyleFormMixin:

    def add_bootstrap_classes(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({"class": "form-control"})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({"class": "form-control"})
            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({"class": "form-control-file"})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({"class": "form-control"})
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({"class": "form-check-input"})
            elif isinstance(field.widget, forms.RadioSelect):
                field.widget.attrs.update({"class": "form-check-input"})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_bootstrap_classes()


FORBIDDEN_WORDS = [
    "казино",
    "криптовалюта",
    "крипта",
    "биржа",
    "дешево",
    "бесплатно",
    "обман",
    "полиция",
    "радар",
]


class ClientForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Client
        fields = [
            "email",
            "first_name",
            "last_name",
            "comment"
        ]

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if any(word in first_name.lower() for word in FORBIDDEN_WORDS):
            raise ValidationError("Имя клиента содержит запрещённые слова.")
        return first_name

    def clean_last(self):
        last_name = self.cleaned_data.get("last_name")
        if any(word in last_name.lower() for word in FORBIDDEN_WORDS):
            raise ValidationError("Фамилия клиента содержит запрещённые слова.")
        return last_name

    def clean_comment(self):
        comment = self.cleaned_data.get("comment")
        if comment and any(word in comment.lower() for word in FORBIDDEN_WORDS):
            raise ValidationError("Комментарий клиента содержит запрещённые слова.")
        return comment
