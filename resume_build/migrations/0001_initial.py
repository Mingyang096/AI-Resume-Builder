# Generated by Django 4.2.16 on 2024-11-23 05:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=32, verbose_name='username')),
                ('password', models.CharField(max_length=64, verbose_name='password')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('country', models.CharField(default='DefaultCountryName', max_length=100)),
                ('city', models.CharField(default='DefaultCityName', max_length=100)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('skills', models.JSONField(default=list)),
            ],
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_year', models.IntegerField()),
                ('start_month', models.IntegerField()),
                ('end_year', models.IntegerField()),
                ('end_month', models.IntegerField()),
                ('institution_name', models.CharField(default='Unknown Institution', max_length=200)),
                ('position', models.CharField(default='Unknown Position', max_length=100)),
                ('department_and_role', models.TextField(default='Not Specified')),
                ('content', models.TextField(blank=True, null=True)),
                ('bullet_points', models.JSONField(default=list)),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='resume_build.user')),
            ],
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_year', models.IntegerField()),
                ('start_month', models.IntegerField()),
                ('end_year', models.IntegerField()),
                ('end_month', models.IntegerField()),
                ('school_name', models.CharField(default='Unknown School', max_length=255)),
                ('major', models.CharField(default='Undeclared Major', max_length=255)),
                ('gpa', models.FloatField(blank=True, null=True)),
                ('scholarships', models.TextField(blank=True, null=True)),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='resume_build.user')),
            ],
        ),
    ]
