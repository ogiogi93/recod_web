from django.db import models
from django.utils.lru_cache import lru_cache

from account.models import CustomUser as User


class Platform(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, unique=True)
    display_name = models.CharField(max_length=255, null=False, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'platforms'
        managed = False

    def __str__(self):
        return self.display_name


class Discipline(models.Model):
    id = models.AutoField(primary_key=True)
    api_discipline_id = models.CharField(max_length=255, null=False, unique=True)
    name = models.CharField(max_length=255, null=False)
    full_name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=30)
    copy_rights = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'disciplines'
        managed = False

    def __str__(self):
        return self.name


class Game(models.Model):
    id = models.AutoField(primary_key=True)
    platform = models.ForeignKey(Platform, on_delete=False)
    discipline = models.ForeignKey(Discipline, on_delete=False)
    thumbnail_url = models.URLField()
    home_url = models.URLField()
    is_active = models.BooleanField(default=True)
    date_released = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'games'
        managed = False
        unique_together = ('discipline', 'platform',)

    def __str__(self):
        return '{} ({})'.format(self.discipline.name, self.platform.display_name)

    @classmethod
    def get_enabled_games(cls):
        return cls.objects.filter(discipline__is_active=True).select_related('discipline', 'platform').all()


class Map(models.Model):
    id = models.AutoField(primary_key=True)
    game = models.ForeignKey(Game, on_delete=False)
    name = models.CharField(max_length=255, null=False)
    thumbnail_url = models.URLField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'maps'
        managed = False
        unique_together = ('game', 'name',)


class Team(models.Model):
    id = models.AutoField(primary_key=True)
    game = models.ForeignKey(Game, on_delete=False)
    name = models.CharField(max_length=255, null=False)
    date_created = models.DateField(auto_now_add=True)
    description = models.TextField(max_length=1024)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='teams/', default='default-team-icon.png')
    website = models.URLField(max_length=255, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'teams'
        managed = False


class MemberManager(models.Manager):
    use_for_related_fields = True

    @staticmethod
    def add_member(user, team, is_admin=False):
        member = Member(user=user, team=team, is_admin=is_admin)
        member.save()


class Member(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=False)
    team = models.ForeignKey(Team, on_delete=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MemberManager()

    class Meta:
        db_table = 'team_members'
        managed = False
        unique_together = (('user', 'team'), ('team', 'is_admin'),)


class MatchFormat(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    display_name = models.CharField(max_length=255, null=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'match_formats'
        managed = False

    def __str__(self):
        return self.display_name

    @classmethod
    @lru_cache(maxsize=1)
    def get_enabled_match_format(cls):
        return cls.objects.filter(is_active=True).all()


class Tournament(models.Model):
    id = models.AutoField(primary_key=True)
    api_tournament_id = models.CharField(max_length=255, null=False)
    name = models.CharField(max_length=30, null=False)
    game = models.ForeignKey(Game, on_delete=False)
    size = models.IntegerField(null=False)
    participant_type = models.CharField(max_length=30, null=False)
    full_name = models.CharField(max_length=80)
    organization = models.CharField(max_length=255)
    website = models.URLField()
    date_start = models.DateField(null=False)
    date_end = models.DateField(null=False)
    online = models.BooleanField(default=True)
    public = models.BooleanField(default=True)
    location = models.CharField(max_length=255)
    country = models.CharField(max_length=2, default='JP')
    description = models.CharField(max_length=1500)
    rules = models.CharField(max_length=10000)
    prize = models.CharField(max_length=1500)
    image = models.ImageField(upload_to='tournaments/')
    is_active = models.BooleanField(default=True)
    match_format = models.ForeignKey(MatchFormat, on_delete=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tournaments'
        managed = False

    def __str__(self):
        return '{}, 開催日: {} ~ {}, ゲーム: {} ({})'.format(
            self.name, self.date_start, self.date_end, self.game.discipline.name, self.game.platform.display_name)


class Stage(models.Model):
    id = models.AutoField(primary_key=True)
    api_stage_id = models.IntegerField(null=False)
    tournament = models.ForeignKey(Tournament, on_delete=False)
    name = models.CharField(max_length=255, null=False)
    type = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'stages'
        managed = False


class Participate(models.Model):
    id = models.AutoField(primary_key=True)
    api_participate_id = models.CharField(max_length=255, null=False)
    tournament = models.ForeignKey(Tournament, on_delete=False)
    team = models.ForeignKey(Team, on_delete=False)
    date_joined = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'participates'
        managed = False


class Match(models.Model):
    id = models.AutoField(primary_key=True)
    api_match_id = models.CharField(max_length=255, null=False)
    game = models.ForeignKey(Game, on_delete=False)
    tournament = models.ForeignKey(Tournament, on_delete=False)
    stage = models.ForeignKey(Stage, on_delete=False)
    group_number = models.IntegerField(null=False)
    round_number = models.IntegerField(null=False)
    match_format = models.ForeignKey(MatchFormat, on_delete=False)
    status = models.CharField(max_length=80, default='pending')
    start_date = models.DateField(default=None)
    start_time = models.TimeField(default=None)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'matches'
        managed = False


class MatchTeam(models.Model):
    id = models.AutoField(primary_key=True)
    match = models.ForeignKey(Match, on_delete=False)
    team = models.ForeignKey(Team, on_delete=False)
    api_opponent_id = models.IntegerField(null=False)
    result = models.IntegerField()
    score = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'match_teams'
        managed = False
