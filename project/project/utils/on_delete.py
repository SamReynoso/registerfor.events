from django.db import models


def on_team_delete(collector, field, sub_objs, using):
    for team in sub_objs:
        team.registrations.filter(
                canceled=False,
                withdrawn=False,
                attended=False
                ).update(withdrawn=True)
    models.SET_NULL(collector, field, sub_objs, using)
