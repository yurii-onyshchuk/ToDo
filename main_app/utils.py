from itertools import chain


def sorting_tasks_queryset(queryset):
    return list(chain(queryset.filter(planned_date__isnull=False).order_by('planned_date'),
                      queryset.filter(planned_date__isnull=True).order_by('-created_date')))
