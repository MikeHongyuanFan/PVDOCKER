from django.db import migrations


class Migration(migrations.Migration):
    """
    This migration is a no-op that exists to resolve the conflict between
    0006_add_solvency_enquiries and 0008_add_solvency_enquiries which both
    add the same fields. Since the fields already exist in the database,
    we don't need to do anything here.
    """

    dependencies = [
        ('applications', '0009_merge_20250513_0009'),
    ]

    operations = [
        # No operations needed since the fields already exist
    ]
