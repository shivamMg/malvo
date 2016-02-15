from django.shortcuts import HttpResponseRedirect, render
from django.core.urlresolvers import reverse

from .forms import TeamCreationForm, TeamMemberCreationFormSet

def register_team(request):
    if request.method == 'GET':
        team_form = TeamCreationForm()
        team_member_formset = TeamMemberCreationFormSet()
        return render(request, 'teams/register.html', {
            'team_form': team_form,
            'team_member_formset': team_member_formset
        })
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
            return HttpResponseRedirect(reverse('mcqs:index'))
        else:
            return render(request, 'teams/register.html', {
                'team_form': team_form,
                'team_member_formset': team_member_formset
            })
