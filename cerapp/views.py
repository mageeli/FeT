# -*- coding: UTF-8 -*-
import ssl

from django.shortcuts import render

from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from django_weasyprint.utils import django_url_fetcher

from weasyprint import HTML
from weasyprint.fonts import FontConfiguration
import functools

from django.conf import settings
from django.views.generic import DetailView

from django_weasyprint import WeasyTemplateResponseMixin
from django_weasyprint.views import CONTENT_TYPE_PNG, WeasyTemplateResponse


# Create your views here.
from .models import Post

def home(request):
    query = request.GET.get('name')
    message = "{}".format(query)
    template = "index.html"
    context = {
        'message': message,
    }
    return render(request, template, context)


class WriteView(generic.CreateView):
    template_name = 'index.html'
    model = Post
    fields = ['name']

    def get_initial(self, ):
        initial = super().get_initial()
        return initial


# def pdf(request):
#     query = request.GET.get('name')
#     message = "{}".format(query)
#     template = "nextone.html"
#     context = {
#         'message': message,
#     }
#     return render(request, template, context)

def pdf(request):
    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = "inline; filename=donation-receipt.pdf".format()
    html = render_to_string("index.html")
    font_config = FontConfiguration()
    HTML(string=html).write_pdf(response, font_config=font_config)
    return response


class MyModelView(generic.DetailView):
    # vanilla Django DetailView
    template_name = 'nextone.html'
    model = Post

class CustomWeasyTemplateResponse(WeasyTemplateResponse):
    # customized response class to change the default URL fetcher
    def get_url_fetcher(self):
        # disable host and certificate check
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        return functools.partial(django_url_fetcher, ssl_context=context)

class MyModelPrintView(WeasyTemplateResponseMixin, MyModelView):
    # output of MyModelView rendered as PDF with hardcoded CSS
    # pdf_stylesheets = [
    #     settings.STATIC_ROOT + '/style.css',
    # ]
    # show pdf in-line (default: True, show download dialog)
    pdf_attachment = True
    # custom response class to configure url-fetcher
    response_class = CustomWeasyTemplateResponse

class MyModelDownloadView(WeasyTemplateResponseMixin, MyModelView):
    # suggested filename (is required for attachment/download!)
    pdf_filename = 'FeT.pdf'

class MyModelImageView(WeasyTemplateResponseMixin, MyModelView):
    # generate a PNG image instead
    content_type = CONTENT_TYPE_PNG

    # dynamically generate filename
    def get_pdf_filename(self):
        return 'mousa.pdf'