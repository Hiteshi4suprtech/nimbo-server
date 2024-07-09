
# nimboapp/views.py

import json
from django.http import JsonResponse, HttpResponse
from django.middleware.csrf import get_token
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from ariadne import graphql_sync, gql, make_executable_schema
from django.conf import settings
from .schema import schema

def csrf_token_view(request):
    return JsonResponse({'csrfToken': get_token(request)})

@method_decorator(csrf_exempt, name='dispatch')
class GraphQLView(View):
    def get(self, request, *args, **kwargs):
        playground_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset=utf-8/>
            <title>GraphQL Playground</title>
            <link rel="stylesheet" href="//cdn.jsdelivr.net/npm/graphql-playground-react@1.7.20/build/static/css/index.css"/>
            <link rel="shortcut icon" href="//cdn.jsdelivr.net/npm/graphql-playground-react@1.7.20/build/favicon.png"/>
            <script src="//cdn.jsdelivr.net/npm/graphql-playground-react@1.7.20/build/static/js/middleware.js"></script>
        </head>
        <body>
            <div id="root"/>
            <script>
                window.addEventListener('load', function (event) {
                    fetch('/csrf_token/')
                        .then(response => response.json())
                        .then(data => {
                            const csrfToken = data.csrfToken;
                            GraphQLPlayground.init(document.getElementById('root'), {
                                endpoint: '/api/nimboql/',
                                settings: {
                                    'request.credentials': 'same-origin',
                                    headers: {
                                        'X-CSRFToken': csrfToken
                                    }
                                }
                            });
                        })
                        .catch(error => console.error('Failed to fetch CSRF token:', error));
                });
            </script>
        </body>
        </html>
        """
        return HttpResponse(playground_html, content_type='text/html')

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        success, result = graphql_sync(
            schema,
            data,
            context_value=request,
            debug=settings.DEBUG
        )
        status_code = 200 if success else 400
        return JsonResponse(result, status=status_code)

