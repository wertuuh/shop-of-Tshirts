import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import (
    DataRequired, Email, Length, EqualTo, ValidationError, StopValidation, Optional
)
from models import User

COMMON_PASSWORDS = {
    "12345678", "123456789", "1234567890", "11111111",
    "password", "password1", "qwerty123", "qwertyui", "iloveyou",
}

FORBIDDEN_EMAIL_CHARS = "`'\""


def clean_email(value):
    return value.strip().lower() if isinstance(value, str) else value


# НОВОЕ: проверка на запрещённые символы в email
def no_forbidden_chars(form, field):
    if field.data and any(ch in field.data for ch in FORBIDDEN_EMAIL_CHARS):
        raise StopValidation("Email не должен содержать символы ` ' \"")


class RegisterForm(FlaskForm):
    email = StringField(
        "Email",
        filters=[clean_email],
        validators=[
            DataRequired(message="Введите email"),
            no_forbidden_chars,
            Email(message="Введите корректный email"),
            Length(max=120, message="Email слишком длинный"),
        ],
    )
    password = PasswordField(
        "Пароль",
        validators=[
            DataRequired(message="Введите пароль"),
            Length(min=8, max=128, message="Пароль: от 8 до 128 символов"),
        ],
    )
    password2 = PasswordField(
        "Повторите пароль",
        validators=[
            DataRequired(message="Повторите пароль"),
            EqualTo("password", message="Пароли не совпадают"),
        ],
    )

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Этот email уже зарегистрирован")

    def validate_password(self, field):
        if field.data.lower() in COMMON_PASSWORDS:
            raise ValidationError("Слишком простой пароль")
        # НОВОЕ: минимум две цифры
        if sum(ch in "0123456789" for ch in field.data) < 2:
            raise ValidationError("Пароль должен содержать минимум 2 цифры")
        if field.data.lower() == (self.email.data or ""):
            raise ValidationError("Пароль не должен совпадать с email")


def clean_text(value):
    return value.strip() if isinstance(value, str) else value

class CheckoutForm(FlaskForm):
    name = StringField(
        "Имя",
        filters=[clean_text],
        validators=[
            DataRequired(message="Введите имя"),
            Length(min=2, max=80, message="Имя: от 2 до 80 символов"),
        ],
    )
    phone = StringField(
        "Телефон",
        filters=[clean_text],
        validators=[
            DataRequired(message="Введите телефон"),
            Length(max=30, message="Телефон слишком длинный"),
        ],
    )
    email = StringField(
        "Email",
        filters=[clean_email],
        validators=[
            DataRequired(message="Введите email"),
            no_forbidden_chars,
            Email(message="Введите корректный email"),
            Length(max=120, message="Email слишком длинный"),
        ],
    )
    address = StringField(
        "Адрес доставки",
        filters=[clean_text],
        validators=[
            DataRequired(message="Введите адрес"),
            Length(min=10, max=250, message="Укажите адрес полностью: город, улица, дом, квартира"),
        ],
    )
    comment = TextAreaField(
        "Комментарий к заказу (необязательно)",
        filters=[clean_text],
        validators=[
            Optional(),
            Length(max=500, message="Не больше 500 символов"),
        ],
    )
    def validate_phone(self, field):
        if not re.fullmatch(r"[0-9+\-()\s]+", field.data):
            raise ValidationError("В телефоне можно только цифры, пробелы, + - и скобки")