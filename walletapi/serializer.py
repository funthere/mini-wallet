from rest_framework import serializers
from .models import Account, Transaction
from rest_framework.fields import Field

class TokenSerializer(serializers.Serializer):
    token_id = serializers.CharField(max_length=50)

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'owned_by', 'status', 'enabled_at', 'balance']

class PostTransactionSerializer(serializers.Serializer):
    amount = serializers.IntegerField(required=True, min_value=0)
    reference_id = serializers.UUIDField(
        required=True,
    )

class TransactionStatusField(Field):
    def __init__(self, *args, **kwargs):
        kwargs["source"] = "*"
        kwargs["read_only"] = True
        super(TransactionStatusField, self).__init__(**kwargs)

    def to_representation(self, transaction):
        return "success" if transaction.status is True else "failure"

class DepositSerializer(serializers.ModelSerializer):
    deposited_by = serializers.UUIDField(source="transaction_by.owned_by", read_only=True)
    status = TransactionStatusField()
    deposited_at = serializers.DateTimeField(source="transaction_time")

    class Meta:
        model = Transaction
        fields = (
            "id",
            "deposited_by",
            "status",
            "deposited_at",
            "amount",
            "reference_id",
        )

class WithdrawalSerializer(serializers.ModelSerializer):
    withdrawn_by = serializers.UUIDField(source="transaction_by.owned_by", read_only=True)
    status = TransactionStatusField()
    withdrawn_at = serializers.DateTimeField(source="transaction_time")

    class Meta:
        model = Transaction
        fields = (
            "id",
            "withdrawn_by",
            "status",
            "withdrawn_at",
            "amount",
            "reference_id",
        )