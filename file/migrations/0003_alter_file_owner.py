# Generated by Django 4.1.13 on 2024-03-30 17:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0002_alter_user_id"),
        ("file", "0002_alter_file_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="file",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="user.user"
            ),
        ),
    ]
