# Generated by Django 4.2.6 on 2023-10-11 02:05

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('walletapi', '0002_alter_account_id_alter_transaction_id_custauthtoken'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='changed_at',
            new_name='enabled_at',
        ),
        migrations.AlterField(
            model_name='account',
            name='id',
            field=models.CharField(default=uuid.UUID('958feb26-67da-11ee-9470-f69c58ab96f9'), max_length=50, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='account',
            name='status',
            field=models.CharField(choices=[('enabled', 'Enabled'), ('disabled', 'Disabled')], default='disabled', max_length=10),
        ),
        migrations.AlterField(
            model_name='custauthtoken',
            name='token_id',
            field=models.CharField(default=uuid.UUID('95900282-67da-11ee-9470-f69c58ab96f9'), max_length=50, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='id',
            field=models.CharField(default=uuid.UUID('958ff846-67da-11ee-9470-f69c58ab96f9'), max_length=50, primary_key=True, serialize=False),
        ),
    ]
