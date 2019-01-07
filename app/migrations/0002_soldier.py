# Generated by Django 2.1.4 on 2019-01-07 15:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Soldier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.CharField(choices=[('unset', '--Unset--'), ('private', 'Private'), ('private_fc', 'Private First Class'), ('lance_c', 'Lance Corporal'), ('nut_c', 'Nut Corporal'), ('sergeant', 'Sergeant'), ('s_sergeant', 'Staff Sergeant'), ('n_sergeant', 'Nut Sergeant'), ('m_sergeant', 'Master Sergeant'), ('lieutenant', 'Lieutenant'), ('captain', 'Captain'), ('major', 'Major'), ('colonel', 'Colonel'), ('general', 'General')], default='unset', max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]