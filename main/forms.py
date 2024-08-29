from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError
from django.utils.timezone import now

from main.models import Client, Message, Mailing


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
        fields = ["email", "first_name", "last_name", "comment"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

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

    def save(self, commit=True):
        client = super().save(commit=False)
        if self.user:
            client.user = self.user
        if commit:
            client.save()
        return client


class MessageForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Message
        fields = [
            "subject",
            "body",
        ]

    def clean_subject(self):
        subject = self.cleaned_data.get("subject")
        if subject and any(word in subject.lower() for word in FORBIDDEN_WORDS):
            raise ValidationError("Комментарий клиента содержит запрещённые слова.")
        return subject

    def clean_body(self):
        body = self.cleaned_data.get("body")
        if body and any(word in body.lower() for word in FORBIDDEN_WORDS):
            raise ValidationError("Комментарий клиента содержит запрещённые слова.")
        return body


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = [
            "clients",
            "message",
            "send_date",
            "end_date",
            "interval",
            "is_active",
        ]
        widgets = {
            "clients": forms.CheckboxSelectMultiple(),
            "message": forms.Select(attrs={"class": "form-control"}),
            "send_date": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
            "end_date": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
            "interval": forms.Select(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        initial_send_date = kwargs.pop("initial_send_date", now())
        initial_end_date = kwargs.pop("initial_end_date", now())
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields["clients"].queryset = Client.objects.filter(user=self.user)

        self.fields["send_date"].initial = initial_send_date
        self.fields["end_date"].initial = initial_end_date

    def save(self, commit=True):
        mailing = super().save(commit=False)
        if self.user:
            mailing.user = self.user
        if commit:
            mailing.save()
            self.save_m2m()
        return mailing


class ManagerMailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ["is_active"]

        widgets = {
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
