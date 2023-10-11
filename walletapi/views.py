from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Account,Transaction, CustAuthToken
from .serializer import TokenSerializer, AccountSerializer, TransactionSerializer
from .decorators import is_autheticated

import logging
import sys,decimal
from datetime import datetime

logging.basicConfig(level=logging.INFO,filename='apiLogs.log')

# Create your views here.
@api_view(['POST',])
def init_wallet(request):
    try:
        if request.method == 'POST':
            customer_xid = request.POST.get('customer_xid')
            account = Account(
                owned_by=customer_xid,
            )
            token = account.create()
            serialized_data = TokenSerializer(token)
            return Response({
                "data": serialized_data.data,
                "status": "success"
                },
                status=200)
    except Exception as ex:
        logging.error("Exception in init wallet : {}".format(str(ex)))
        return Response({"error":"Internal Server Error"}, status=500)


@api_view(['POST','GET','PATCH'])
@is_autheticated
def enable_wallet(request):
    try:
        session = get_session(token_id = request.headers.get('Authorization'))
        if request.method == "POST":
            if session['account'].status == 'E':
                return Response({
                    "status" : "fail",
                    "data" : {"error" : "Already Enabled"}
                })
            session['account'].status = 'E'
            session['account'].changed_at = datetime.now().isoformat()
            session['account'].save()
            serialized_acc_data = AccountSerializer(session['account'])
            return Response({"status":"success","data":{"wallet":serialized_acc_data.data}})

        elif request.method == "GET":
            if session['account'].status == 'D':
                 return Response({
                    "status" : "fail",
                    "data" : {"error" : "Account is Disabled"}
                })
            serialized_acc_data = AccountSerializer(session['account'])
            return Response({"status":"success","data":{"wallet":serialized_acc_data.data}})

    except Exception as ex:
        logging.error("Exception in Enable wallet {}".format(str(ex)))
        return Response({"error":"Internal Server Error"},status=500)

def get_session(token_id):
    user_token = CustAuthToken.objects.get(token_id = token_id)
    account = Account.objects.get(id = user_token.user.id)
    return {"user_token":user_token,"account":account}
