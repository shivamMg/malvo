from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _

from .models import Team, TeamMember, UploadFileModel


class TeamCreationForm(forms.ModelForm):
    """
    Create team from team_name and password
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation',
                                widget=forms.PasswordInput)

    class Meta:
        model = Team
        fields = ('team_name', 'lang_pref')
        labels = {
            'team_name': 'Team Name',
            'lang_pref': 'Programming Language',
        }
        widgets = {
            'lang_pref': forms.RadioSelect,
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        team = super(TeamCreationForm, self).save(commit=False)
        team.set_password(self.cleaned_data["password1"])
        if commit:
            team.save()
        return team


class TeamChangeForm(forms.ModelForm):
    """
    A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Team
        fields = ('team_name', 'password',)

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial['password']


class TeamMemberCreationForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ('full_name', 'college_id', 'mobile_no', 'email')
        labels = {
            'full_name': _('Full Name'),
            'college_id': _('College ID'),
            'mobile_no': _('Mobile Number'),
            'email': _('Email'),
        }


class TeamMemberChangeForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ('full_name', 'college_id', 'mobile_no', 'email')
        labels = {
            'full_name': _('Full Name'),
            'college_id': _('College ID'),
            'mobile_no': _('Mobile Number'),
            'email': _('Email'),
        }


TeamMemberCreationFormSet = forms.formset_factory(TeamMemberCreationForm, extra=2)


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadFileModel

        fields = ('file',)
        labels = {
            'file': 'Upload File',
        }
        widgets = {
            'file': forms.FileInput(attrs={'required': 'true'})
        }
