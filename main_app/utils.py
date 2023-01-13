from itertools import chain


def sorting_tasks_queryset(queryset):
    return list(chain(queryset.filter(date__isnull=False).order_by('date'),
                      queryset.filter(date__isnull=True).order_by('-created_data')))
