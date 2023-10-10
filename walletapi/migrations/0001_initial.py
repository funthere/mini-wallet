# Generated by Django 4.2.6 on 2023-10-10 13:28

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.CharField(default=uuid.UUID('ec3e94e6-6770-11ee-8c54-f69c58ab96f9'), max_length=50, primary_key=True, serialize=False)),
                ('owned_by', models.CharField(max_length=50)),
                ('status', models.CharField(choices=[('E', 'Enabled'), ('D', 'Disabled')], default='D', max_length=10)),
                ('changed_at', models.DateTimeField(null=True)),
                ('balance', models.DecimalField(decimal_places=2, max_digits=15)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.CharField(default=uuid.UUID('ec3e9f2c-6770-11ee-8c54-f69c58ab96f9'), max_length=50, primary_key=True, serialize=False)),
                ('transaction_type', models.CharField(max_length=20)),
                ('transaction_time', models.DateTimeField(null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('reference_id', models.CharField(max_length=50, unique=True)),
                ('transaction_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='walletapi.account')),
            ],
        ),
    ]
