from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinLengthValidator


class TeamManager(BaseUserManager):

    def create_user(self, team_name, password):
        """
        Creates and saves team with given `team_name` and `password`
        """
        if not team_name:
            raise ValueError('Team must have a team name')

        team = self.model(team_name=team_name)
        team.set_password(password)
        team.save(using=self._db)
        return team

    def create_superuser(self, team_name, password):
        """
        Creates a superuser team
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
    Team with a team name and language preference
    """
    PROG_LANGS = (
        ('C', 'C'),
        ('J', 'Java'),
    )

    team_name = models.SlugField(_('team name'), max_length=25, unique=True)
    lang_pref = models.CharField(_('programming language preference'),
                                 max_length=1, choices=PROG_LANGS, default='0')
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
    Team Member belonging to a Team
    """
    full_name = models.CharField(_('full name'), max_length=25)
    mobile_no = models.CharField(
        _('mobile number'),
        max_length=15,
        validators=[MinLengthValidator(10, 'Invalid Mobile Number')]
    )
    email = models.EmailField(_('email address'), max_length=50)
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
    Answer to an MCQ by a Team
    """
    question_no = models.IntegerField()
    # id of the choice selected
    choice_id = models.IntegerField(default=0)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('question_no', 'team',)

    def __str__(self):
        return "Q{0} Ans:{1}".format(self.question_no, self.choice_id)


class TeamCodingAnswer(models.Model):
    """
    Answer to a Coding Question by a Team
    """
    question_no = models.IntegerField()
    input_case_no = models.IntegerField()
    output_text = models.TextField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('team', 'question_no', 'input_case_no',)

    def __str__(self):
        return 'Q{} Input-case:{} Ans:{}'.format(self.question_no,
                                                 self.input_case_no,
                                                 self.output_text[:60])
