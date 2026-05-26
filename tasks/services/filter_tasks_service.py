def filter_tasks(queryset, get_params):
    search_query = get_params.get("search")
    priority_query = get_params.get("priority")

    if search_query:
        queryset = queryset.filter(title__icontains=search_query)
    if priority_query:
        queryset = queryset.filter(priority=priority_query)

    return queryset
