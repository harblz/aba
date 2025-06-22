from django.http import HttpResponse


class HtmxRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if (
            request.htmx
            and response.status_code in [301, 302]
            and response.has_header("Location")
        ):

            location = response["Location"]
            response = HttpResponse()
            response["HX-Redirect"] = location
            return response

        return response
