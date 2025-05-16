from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_user_managers'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=255)),
                ('sent_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('sent', 'Sent'), ('delivered', 'Delivered'), ('opened', 'Opened'), ('clicked', 'Clicked'), ('bounced', 'Bounced'), ('failed', 'Failed')], default='sent', max_length=20)),
                ('message_body', models.TextField(blank=True, null=True)),
                ('email_type', models.CharField(blank=True, max_length=100, null=True)),
                ('notification', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.notification')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='email_logs', to='users.user')),
            ],
            options={
                'verbose_name': 'Email Log',
                'verbose_name_plural': 'Email Logs',
                'ordering': ['-sent_at'],
            },
        ),
    ]
