from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import TextInput, EmailInput, PasswordInput, CharField, DecimalField, NumberInput

from cliente.models import Cliente


class RegisterForm(UserCreationForm):
    """
    Form for registering a new user, with no privileges, from the given username, email and
    password.
    """
    password1 = CharField(
        label="Password",
        strip=False,
        widget=PasswordInput(attrs={"autocomplete": "new-password", "class": "form-control", }),
    )
    password2 = CharField(
        label="Password confirmation",
        widget=PasswordInput(attrs={"autocomplete": "new-password", "class": "form-control", }),
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )

    dni = DecimalField(
        label="ID Number",
        widget=NumberInput(attrs={"class": "form-control", "placeholder": '99.999.999'}),
        min_value=0,
        step_size=1,
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'dni']
        widgets = {
            'username': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'John.D0e',
            }),
            'first_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'John',
                'maxlength': '150',
                'required': 'true',
            }),
            'last_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Doe',
                'maxlength': '150',
                'required': 'true',
            }),
            'email': EmailInput(attrs={'class': 'form-control',
                                       'placeholder': 'your@mail.com',
                                       }),
        }

    def save_customer(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            costumer = Cliente(user=user, dni=self.cleaned_data['dni'])
            costumer.save()
        return user
