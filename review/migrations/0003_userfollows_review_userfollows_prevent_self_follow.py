# Generated by Django 4.0.3 on 2022-04-06 15:32

from django.db import migrations, models
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0002_alter_ticket_options'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='userfollows',
            constraint=models.CheckConstraint(check=models.Q(('user', django.db.models.expressions.F('followed_user')), _negated=True), name='review_userfollows_prevent_self_follow'),
        ),
    ]
