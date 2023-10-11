from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Account, CustAuthToken, Transaction
from .serializer import DepositSerializer, PostTransactionSerializer, TokenSerializer, AccountSerializer, WithdrawalSerializer
from .decorators import is_autheticated
from django.utils import timezone
from django.db import transaction

import decimal
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


@api_view(['POST'])
@is_autheticated
def deposit(request):
    session = get_session(token_id = request.headers.get('Authorization'))
    if request.method == "POST":
        serializer = PostTransactionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "status" : "fail",
                "data" : serializer.errors
                })

        if session['account'].status == 'disabled':
            return Response({
                "status" : "fail",
                "data" : {"error" : "Account is Disabled"}
                })
        elif not check_reference_id(reference_id):
            return Response({
                "status" : "fail",
                "data" : {"referance_id" : "referance_id not unique"}
                })

        amount = request.data.get("amount")
        reference_id = request.data.get("reference_id")

        with transaction.atomic():
            tr = Transaction(
                transaction_by = session['account'],
                transaction_type = "Deposit",
                transaction_time = timezone.now(),
                amount = amount,
                reference_id = reference_id
            )
            session['account'].balance += decimal.Decimal(amount)
            session['account'].save()
            tr.save()

        serialized_tr = DepositSerializer(tr)

        return Response({"status":"success", "data": {"deposit": serialized_tr.data}}, status = 201)


@api_view(['POST'])
@is_autheticated
def withdraw(request):
    session = get_session(token_id = request.headers.get('Authorization'))

    serializer = PostTransactionSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({
            "status" : "fail",
            "data" : serializer.errors
            })
    amount = decimal.Decimal(request.POST.get('amount'))
    reference_id = request.POST.get('reference_id')

    if session['account'].status == 'disabled':
        return Response({
            "status" : "fail",
            "data" : {"error" : "Account is Disabled"}
            })

    elif amount > session['account'].balance:
        return Response({"status": "fail", "data": {"error": "Insufficient Funds"}})

    elif not check_reference_id(reference_id):
        return Response({
            "status" : "fail",
            "data" : {"error" : "referance_id not unique"}
            })

    with transaction.atomic():
        tr = Transaction(
            transaction_by = session['account'],
            transaction_type = "Withdrawal",
            transaction_time = timezone.now(),
            amount = amount,
            reference_id = reference_id
        )
        session['account'].balance = session['account'].balance - amount
        session['account'].save()
        tr.save()

    serialized_tr = WithdrawalSerializer(tr)

    return Response({"status": "success", "data": {"withdrawal": serialized_tr.data}}, status = 201)

def check_reference_id(reference_id):
    try:
        tr = Transaction.objects.get(reference_id = reference_id)
        if tr:
            return False
        return True
    except:
        return True

def get_session(token_id):
    token_id = str(token_id).lstrip('Token ')
    user_token = CustAuthToken.objects.get(token_id = token_id)
    account = Account.objects.get(id = user_token.user.id)

    return {"user_token": user_token, "account": account}