from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('borrowers', '0004_rename_phone_guarantor_address_street_no_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='bg_type',
            field=models.CharField(
                choices=[('bg1', 'B/G1'), ('bg2', 'B/G2')],
                default='bg1',
                help_text='Indicates if this asset belongs to B/G1 or B/G2',
                max_length=10
            ),
        ),
        migrations.AddField(
            model_name='liability',
            name='bg_type',
            field=models.CharField(
                choices=[('bg1', 'B/G1'), ('bg2', 'B/G2')],
                default='bg1',
                help_text='Indicates if this liability belongs to B/G1 or B/G2',
                max_length=10
            ),
        ),
    ]
