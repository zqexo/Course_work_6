from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from blog.models import Blog


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


class BlogForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Blog
        fields = ["title", "content", "image"]

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if any(word in title.lower() for word in FORBIDDEN_WORDS):
            raise ValidationError("Заголовок содержит запрещённые слова.")
        return title

    def clean_content(self):
        content = self.cleaned_data.get("content")
        if content and any(word in content.lower() for word in FORBIDDEN_WORDS):
            raise ValidationError("Содержимое статьи содержит запрещённые слова.")
        return content
