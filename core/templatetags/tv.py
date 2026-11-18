"""Filtros de template para aplicar as classes do Bootstrap nos campos dos formulários."""

from django import forms, template

register = template.Library()


@register.filter
def bs(field):
    """Renderiza o campo com a classe Bootstrap adequada e marca erros (is-invalid)."""
    widget = field.field.widget
    if isinstance(widget, (forms.CheckboxInput,)):
        classe = 'form-check-input'
    elif isinstance(widget, forms.CheckboxSelectMultiple):
        classe = ''
    elif isinstance(widget, (forms.Select, forms.SelectMultiple)):
        classe = 'form-select'
    else:
        classe = 'form-control'
    if field.errors:
        classe += ' is-invalid'
    atuais = widget.attrs.get('class', '')
    return field.as_widget(attrs={'class': f'{atuais} {classe}'.strip()})


@register.filter
def is_checkbox(field):
    return isinstance(field.field.widget, forms.CheckboxInput)


@register.filter
def is_multicheck(field):
    return isinstance(field.field.widget, forms.CheckboxSelectMultiple)
