from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    """
    Entidade USUARIO do modelo de dados.

    Herda do usuário padrão do Django (senha com hash, is_staff, date_joined...)
    e troca o login para ser feito pelo e-mail, como descrito no UC01.
    """

    email = models.EmailField('e-mail', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'usuário'
        verbose_name_plural = 'usuários'

    def __str__(self):
        return self.email
