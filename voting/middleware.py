from django.shortcuts import render
from django.urls import Resolver404, resolve


class Custom404Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            resolve(request.path_info)
        except Resolver404:
            return render(request, '404.html', status=404)
        response = self.get_response(request)
        return response