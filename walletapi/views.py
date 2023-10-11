from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Account, CustAuthToken
from .serializer import TokenSerializer, AccountSerializer
from .decorators import is_autheticated
from django.utils import timezone

import logging

logging.basicConfig(level=logging.INFO,filename='apiLogs.log')

# Create your views here.
@api_view(['POST'])
def init_wallet(request):
    try:
        if request.method == 'POST':
            customer_xid = request.POST.get('customer_xid')
            statusCode = 200
            account = Account.objects.filter(owned_by = customer_xid).first()
            if account and account.id != '':
                token = CustAuthToken.objects.filter(user = account).first()
            else:
                account = Account(owned_by = customer_xid)
                token = account.create()
                statusCode = 201

            serialized_data = TokenSerializer(token)
            return JsonResponse({
                    "status": "success",
                    "data": serialized_data.data
                }, status = statusCode
            )
    except Exception as ex:
        logging.error("Exception in init wallet : {}".format(str(ex)))
        return JsonResponse({"status": "error", "message": "Internal Server Error"}, status = 500)


@api_view(['POST', 'GET', 'PATCH'])
@is_autheticated
def enable_wallet(request):
    try:
        session = get_session(token_id = request.headers.get('Authorization'))
        if request.method == "POST":
            if session['account'].status == 'enabled':
                return JsonResponse({
                    "status" : "fail",
                    "data" : {"error" : "Already Enabled"}
                })
            session['account'].status = 'enabled'
            session['account'].enabled_at = timezone.now()
            session['account'].save()
            serialized_acc_data = AccountSerializer(session['account'])

            return JsonResponse({"status":"success", "data":{"wallet":serialized_acc_data.data}}, status = 201)

        elif request.method == "GET":
            if session['account'].status == 'disabled':
                 return JsonResponse({
                    "status" : "fail",
                    "data" : {"error" : "Account is Disabled"}
                })
            serialized_acc_data = AccountSerializer(session['account'])

            return JsonResponse({"status":"success", "data":{"wallet":serialized_acc_data.data}})

    except Exception as ex:
        logging.error("Exception in Enable wallet {}".format(str(ex)))
        return JsonResponse({"status": "error", "message":"Internal Server Error"}, status = 500)

def get_session(token_id):
    user_token = CustAuthToken.objects.get(token_id = token_id)
    account = Account.objects.get(id = user_token.user.id)

    return {"user_token":user_token, "account":account}
