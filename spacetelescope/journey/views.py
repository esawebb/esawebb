from django.shortcuts import render

from django.http import JsonResponse
from django.views.generic.base import TemplateView

# Create your views here.
class JourneyView(TemplateView):

    template_name = 'journey.html'

    def get_context_data(self, **kwargs):
        context = super(JourneyView, self).get_context_data(**kwargs)

        return context

class SoonView(TemplateView):

    template_name = 'soon.html'

    def get_context_data(self, **kwargs):
        context = super(SoonView, self).get_context_data(**kwargs)

        return context