from django.db import migrations


class Migration(migrations.Migration):
    """
    This migration is now empty because the fields were already added to the database.
    We keep this file to maintain migration history and dependencies.
    """

    dependencies = [
        ('applications', '0005_add_funding_calculation'),
    ]

    operations = [
        # No operations needed since the fields already exist in the database
    ]
