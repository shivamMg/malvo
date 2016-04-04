from django.shortcuts import HttpResponseRedirect, render, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from .forms import TeamCreationForm, TeamMemberCreationFormSet
from .models import Team


def register_team(request):
    if request.method == 'GET':
        team_form = TeamCreationForm()
        team_member_formset = TeamMemberCreationFormSet()
    elif request.method == 'POST':
        team_form = TeamCreationForm(request.POST)
        team_member_formset = TeamMemberCreationFormSet(request.POST)

        if team_form.is_valid() and team_member_formset.is_valid():
            t = team_form.save()
            for form in team_member_formset:
                tm = form.save(commit=False)
                # Set foreignkey to team
                tm.team = t
                tm.save()
            return HttpResponseRedirect(reverse('teams:login'))

    return render(request, 'teams/register.html', {
        'team_form': team_form,
        'team_member_formset': team_member_formset,}
    )


@login_required
def profile(request):
    team = get_object_or_404(Team, team_name=request.user)

    member_list = []

    for member in team.teammember_set.all():
        if member.full_name != '':
            member_list.append({
                'full_name': member.full_name,
                'email': member.email,
                'mobile_no': member.mobile_no,}
            )

    return render(request, 'teams/profile.html', {
        'team_name': team.team_name,
        'lang_pref': team.get_lang_pref_name(),
        'member_list': member_list,}
    )
