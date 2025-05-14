from django.db import migrations


class Migration(migrations.Migration):
    """
    This migration is intentionally empty because the fields were already added
    in 0006_add_solvency_enquiries. We keep this file to maintain migration history
    and dependencies.
    """

    dependencies = [
        ('applications', '0007_application_additional_comments_and_more'),
    ]

    operations = [
        # No operations needed since the fields were added in 0006_add_solvency_enquiries
    ]
