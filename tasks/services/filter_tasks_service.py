from django.db.models import QuerySet
from django.http import QueryDict


def filter_tasks(queryset: QuerySet, get_params: QueryDict) -> QuerySet:
    search_query = get_params.get("search")
    priority_query = get_params.get("priority")

    if search_query:
        queryset = queryset.filter(title__icontains=search_query)
    if priority_query:
        queryset = queryset.filter(priority=priority_query)

    return queryset
