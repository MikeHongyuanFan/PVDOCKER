from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('applications', '0013_application_has_been_bankrupt_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='assigned_bd',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_applications', to=settings.AUTH_USER_MODEL),
        ),
    ]