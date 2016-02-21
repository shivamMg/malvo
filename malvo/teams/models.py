from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class TeamManager(BaseUserManager):
    """
    Manager for a Team.
    """

    def create_user(self, team_name, password):
        """
        Creates and saves team with given `team_name` and `password`.
        """
        if not team_name:
            raise ValueError('Team must have a team name')

        team = self.model(team_name=team_name)
        team.set_password(password)
        team.save(using=self._db)
        return team

    def create_superuser(self, team_name, password):
        """
        Creates a superuser team.
        """
        team = self.create_user(
            team_name=team_name,
            password=password
        )
        team.is_admin = True
        team.save(using=self._db)
        return team


class Team(AbstractBaseUser):
    """
    Team with a Team name.
    """
    team_name = models.SlugField(_('team name'), max_length=25, unique=True)

    is_active = models.BooleanField(_('active'), default=True)
    is_admin = models.BooleanField(_('admin status'), default=False)

    objects = TeamManager()

    USERNAME_FIELD = 'team_name'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('team')
        verbose_name_plural = _('teams')

    def get_full_name(self):
        return self.team_name

    def get_short_name(self):
        return self.team_name

    def get_absolute_url(self):
        return "/teams/{0}".format(self.team_name)

    def __str__(self):
        return self.team_name

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the apps?"""
        return True

    @property
    def is_staff(self):
        """User belongs to staff if he is an admin"""
        return self.is_admin


class TeamMember(models.Model):
    """
    Team Member belonging to a Team.
    """
    full_name = models.CharField(_('full name'), max_length=25)
    mobile_no = models.CharField(_('mobile number'), max_length=15)
    email = models.EmailField(_('email address'), max_length=40)
    team = models.ForeignKey(Team)

    USERNAME_FIELD = 'full_name'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('team member')
        verbose_name_plural = _('team members')

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.full_name

    def __str__(self):
        return self.full_name


class TeamMcqAnswer(models.Model):
    """
    Answer to an MCQ by a Team.
    """
    question_no = models.IntegerField()
    # Text of the answer/choice selected
    choice_text = models.CharField(max_length=1000)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('question_no', 'team',)

    def __str__(self):
        return "Q{0} Ans:{1}".format(self.question_no, self.choice_text)
