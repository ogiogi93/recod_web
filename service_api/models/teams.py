from django.db import models

from account.models import CustomUser as User
from service_api.models.disciplines import Game


class Team(models.Model):
    id = models.AutoField(primary_key=True)
    game = models.ForeignKey(Game, on_delete=False)
    name = models.CharField(max_length=255, null=False)
    date_created = models.DateField(auto_now_add=True)
    description = models.TextField(max_length=1024)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='teams/', default='default-team-icon.png')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'teams'
        managed = False

    @classmethod
    def get_all_teams_with_organizer(cls):
        """
        全チームのインスタンスを返す
        メンバー全員のニックネームを並べた文字列を含めている
        :rtype List[Team]:
        """
        teams = cls.objects.select_related('game', 'game__discipline', 'game__platform') \
            .filter(game__discipline__is_active=True).all()
        for team in teams:
            team.organizer = str(Member.objects.select_related('user').values_list('user__nickname', flat=True)
                                 .filter(team=team)
                                 .filter(is_admin=True).first())
            team.members = str(','.join([nickname for nickname in Member.objects.select_related('user')
                                        .values_list('user__nickname', flat=True)
                                        .filter(team=team)]))
        return teams


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

    @classmethod
    def get_joined_teams(cls, user_id):
        return [(m.team, m.is_admin) for m in
                Member.objects.filter(user_id=user_id).all()]

    @classmethod
    def get_candidate_teams(cls, user_id):
        return [(m.team.id, m.team.teamname) for m in
                Member.objects.exclude(team__id__in=Member.objects.values_list('team__id', flat=True)
                                       .filter(user_id=user_id)
                                       ).all()]
