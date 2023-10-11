import logging
import sys
from rest_framework.response import Response

from .models import CustAuthToken

def is_autheticated(fn):

    def authenticate(request, **kwargs):
        auth_token = request.headers.get('Authorization')
        # since value of Authorization: Token xxxtokenxxx, so trim the Token
        auth_token = str(auth_token).lstrip('Token ')

        try:
            if auth_token:
                user_session = CustAuthToken.objects.get(token = auth_token)
            else:
                return Response({"status": "fail", "message": "No Authorization token"}, status=401)
        except:
            ex_type, ex_val, tr = sys.exc_info()
            if "DoesNotExist" in str(ex_type):
                return Response({"status": "fail", "message": "Authorization token Invalid"}, status=401)
            else:
                logging.error("{0}: {1}".format(str(ex_type), str(ex_val)))
                return Response({"status": "error", "message": "Internal server Error"}, status=500)
        return fn(request, **kwargs)

    return authenticate
