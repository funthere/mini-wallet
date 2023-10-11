import uuid
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APILiveServerTestCase

from .models import Account
# Create your tests here.

class TestWallet(APILiveServerTestCase):
    def setUp(self) -> None:
        self.customer_xid = 'ea0212d3-abd6-406f-8c67-868e814a2437'
        self.reference_id = uuid.uuid4()
        # Init account
        account = Account(owned_by = self.customer_xid)
        self.token = account.create()

    def test_001_wallet_initialize_api_url(self):
        with self.subTest('Success Init'):
            response = self.client.post(
                reverse('api-init'),
                data={'customer_xid': self.customer_xid}
            )
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            response_data = response.json().get('data', {})
            self.assertIsNotNone(response_data.get('token'))
            self.assertEqual(response.json().get('status'), 'success')
            self.assertEqual(Account.objects.count(), 1)

        with self.subTest('Error Init - Missing customer_xid'):
            response = self.client.post(
                reverse('api-init')
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.json().get('status'), 'fail')

    def test_002_wallet_api_url(self):
        """Wallet__api_url."""

        # Success Case
        response = self.client.get(
            reverse('api-wallet'),
            headers={'Authorization': 'Token ' + str(self.token.token)}
        )
        self.assertEqual(response.status_code, 200)

        # Error Case
        response = self.client.get(reverse('api-wallet'))
        self.assertEqual(response.status_code, 500)

    def test_003_enable_wallet_api_url(self):
        """Wallet_enable_api_url."""

        # Success Case
        response = self.client.post(
            reverse('api-wallet'),
            headers={'Authorization': 'Token ' + str(self.token.token)}
        )
        # print(response.json())
        self.assertEqual(response.status_code, 201)

        # Error Case
        response = self.client.get(reverse('api-wallet'))
        self.assertEqual(response.status_code, 500)

    def test_004_wallet_deposit_api_url(self):
        """Wallet_deposit_api_url."""

        wallet = Account.objects.filter(id = self.token.user.id).first()
        wallet.status = 'enabled'
        wallet.save()
        balance = wallet.balance

        # Success Case
        response = self.client.post(
            reverse('api-deposit'),
            headers={'Authorization': 'Token ' + str(self.token.token)},
            data={
                'amount':100,
                'reference_id':"95fc54b6-998f-4197-90b5-ef9871515250"
            }
        )
        walletnew = Account.objects.filter(id = self.token.user.id).first()
        self.assertEqual(response.status_code, 201)
        self.assertGreaterEqual(walletnew.balance, balance)

        # Error Case
        response = self.client.post(
            reverse('api-deposit'),
            headers={'Authorization': 'Token ' + str(self.token.token)}
        )
        self.assertEqual(response.json().get('status'), 'fail')
        self.assertEqual(response.status_code, 200)

    def test_005_wallet_withdraw_api_url(self):
        """Wallet_withdraw_api_url."""

        wallet = Account.objects.filter(id = self.token.user.id).first()

        # Success Case
        response = self.client.post(
            reverse('api-withdraw'),
            headers={'Authorization': 'Token ' + str(self.token.token)},
            data={
                'amount':100,
                'reference_id':"95fc54b6-998f-4197-90b5-ef9871515250"
            }
        )
        walletnew = Account.objects.filter(id = self.token.user.id).first()
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(walletnew.balance, wallet.balance-100)

        # Error Case
        response = self.client.post(
            reverse('api-withdraw'),
            headers={'Authorization': 'Token ' + str(self.token.token)}
        )
        self.assertEqual(response.json().get('status'), 'fail')
        self.assertEqual(response.status_code, 200)

    def test_006_disable_wallet_api_url(self):
        """Wallet_disable_api_url."""

        # Success Case
        response = self.client.patch(
            reverse('api-wallet'),
            headers={'Authorization': 'Token ' + str(self.token.token)}
        )
        self.assertEqual(response.status_code, 200)

        # Error Case
        response = self.client.delete(
            reverse('api-wallet'),
            headers={'Authorization': 'Token ' + str(self.token.token)}
        )
        self.assertEqual(response.status_code, 405)

    def test_007_wallet_deposit_on_disabled_wallet_api_url(self):
        """Deposit_on_disabled_wallet_api_url."""

        wallet = Account.objects.filter(id = self.token.user.id).first()
        wallet.status = 'disabled'
        wallet.save()

        response = self.client.post(
            reverse('api-deposit'),
            headers={'Authorization': 'Token ' + str(self.token.token)},
            data={
                'amount':100,
                'reference_id':"95fc54b6-998f-4197-90b5-ef9871515250"
            }
        )
        content = response.json()
        self.assertEqual(response.status_code, 200)

        self.assertEqual(content['status'], 'fail')
        self.assertEqual(content['data']['error'], 'Account is Disabled')

    def test_008_wallet_transaction_url(self):
        """Wallet__api_wallet_transaction_url."""

        # Success Case
        response = self.client.get(
            reverse('api-list-transaction'),
            headers={'Authorization': 'Token ' + str(self.token.token)}
        )
        self.assertEqual(response.status_code, 200)