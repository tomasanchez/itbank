from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render


def index(request: WSGIRequest) -> HttpResponse:
    """
    View function for Me Page of site.
    """
    template_name: str = 'index.html'
    context: dict = {}
    return render(request, template_name, context)
