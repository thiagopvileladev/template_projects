from django.shortcuts import render


def home(request):
    """Página inicial. Por enquanto só confirma que o projeto está no ar."""
    return render(request, 'core/home.html')
