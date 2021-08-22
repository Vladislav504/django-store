from django.views.generic import TemplateView
from django.http.response import HttpResponse
from .exceptions import ResponseException


class BaseView(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except ResponseException as e:
            return HttpResponse(str(e), status=e.status)
        except Exception as e:
            return HttpResponse(str(e), status=500)
