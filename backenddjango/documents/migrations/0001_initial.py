# Generated by Django 4.2.20 on 2025-04-20 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('document_type', models.CharField(choices=[('indicative_letter', 'Indicative Letter'), ('disbursement', 'Disbursement'), ('application_form', 'Application Form'), ('id_verification', 'ID Verification'), ('financial_statement', 'Financial Statement'), ('property_valuation', 'Property Valuation'), ('other', 'Other')], max_length=50)),
                ('file', models.FileField(upload_to='documents/')),
                ('version', models.PositiveIntegerField(default=1)),
                ('notes', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Fee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fee_type', models.CharField(choices=[('application', 'Application Fee'), ('valuation', 'Valuation Fee'), ('legal', 'Legal Fee'), ('settlement', 'Settlement Fee'), ('other', 'Other Fee')], max_length=50)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('waiting', 'Waiting'), ('paid', 'Paid')], default='waiting', max_length=20)),
                ('invoice', models.FileField(blank=True, null=True, upload_to='invoices/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ledger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('fee_payment', 'Fee Payment'), ('repayment', 'Loan Repayment'), ('disbursement', 'Loan Disbursement'), ('other', 'Other')], max_length=50)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField()),
                ('transaction_date', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('remind_date', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Repayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('due_date', models.DateField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('scheduled', 'Scheduled'), ('paid', 'Paid'), ('late', 'Late'), ('missed', 'Missed')], default='scheduled', max_length=20)),
                ('invoice', models.FileField(blank=True, null=True, upload_to='repayment_invoices/')),
                ('payment_date', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
