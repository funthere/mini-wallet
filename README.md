### Features
<hr>

1. Initialize wallet account
2. Enable & disabled wallet
3. View wallet balance
4. View wallet transactions
5. Deposit & withdrawn money

### Requirements
<hr>

1. Python 3.8+
2. Linux or Mac for best practice

## Setup

Here is a step to get the app up and running in your machine:

Clone the project:

```shell
git clone https://github.com/funthere/mini-wallet

cd mini-wallet
```

Create Python virtual enviroment:

```shell
python3 -m venv venv
```

Activate virtual enviroment (this command can change based on OS):

```shell
source venv/bin/activate
```

Install libs dependencies using pip:

```shell
pip3 install -r requirements.txt
```

Run DB migration:

```shell
python manage.py migrate
```

Start server API:

```shell
python manage.py runserver
```

Now the API is running on http://localhost:8000
You can test the API spec based on this [Mini Wallet Exercise](https://documenter.getpostman.com/view/8411283/SVfMSqA3?version=latest)