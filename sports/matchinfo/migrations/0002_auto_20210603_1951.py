# Generated by Django 3.2 on 2021-06-03 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matchinfo', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='package',
            options={'verbose_name_plural': '详情表'},
        ),
        migrations.RemoveField(
            model_name='package',
            name='name',
        ),
        migrations.AddField(
            model_name='package',
            name='a_match_score',
            field=models.IntegerField(default=0, verbose_name='客队进球'),
        ),
        migrations.AddField(
            model_name='package',
            name='a_player_set',
            field=models.CharField(default='', max_length=100, verbose_name='客队员表'),
        ),
        migrations.AddField(
            model_name='package',
            name='a_team_name',
            field=models.CharField(default='', max_length=50, verbose_name='客队伍名'),
        ),
        migrations.AddField(
            model_name='package',
            name='h_match_score',
            field=models.IntegerField(default=0, verbose_name='主队进球'),
        ),
        migrations.AddField(
            model_name='package',
            name='h_player_set',
            field=models.CharField(default='', max_length=100, verbose_name='主队员表'),
        ),
        migrations.AddField(
            model_name='package',
            name='h_team_name',
            field=models.CharField(default='', max_length=50, verbose_name='主队伍名'),
        ),
        migrations.AddField(
            model_name='package',
            name='match_loc',
            field=models.CharField(default='', max_length=50, verbose_name='比赛地点'),
        ),
        migrations.AddField(
            model_name='package',
            name='match_no',
            field=models.IntegerField(default=0, verbose_name='比赛编号'),
        ),
        migrations.AddField(
            model_name='package',
            name='match_time',
            field=models.CharField(default='', max_length=50, verbose_name='比赛时间'),
        ),
    ]
