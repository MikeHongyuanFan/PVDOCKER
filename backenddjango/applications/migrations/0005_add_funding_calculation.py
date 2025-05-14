# Generated manually

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.contrib.postgres.fields import JSONField


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('applications', '0004_application_stage_last_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='funding_result',
            field=JSONField(blank=True, help_text='Stores the current funding calculation result', null=True),
        ),
        migrations.CreateModel(
            name='FundingCalculationHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calculation_input', JSONField(help_text='Full set of manual input fields used during calculation')),
                ('calculation_result', JSONField(help_text='Computed funding breakdown (all fees, funds available)')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='funding_calculations', to='applications.Application')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='funding_calculations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Funding calculation histories',
                'ordering': ['-created_at'],
            },
        ),
    ]