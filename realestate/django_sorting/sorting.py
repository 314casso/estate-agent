from operator import attrgetter

def queryset_sort(queryset, order_by):
    use_sorted = False
    # If all order_by fields are model fields, use the ORM order_by() method.
    for attr_or_field in order_by:
        name = attr_or_field.strip('-')
        model_class = queryset.model
        
        # Is it an attribute?
        attribute = getattr(model_class, name, None)
        if attribute:
            use_sorted = True
        # Or a field?
        else:
            # Make sure the field exists before sorting
            field_names = [f.attname for f in model_class._meta._fields()]
            if name not in field_names:
                return queryset

    if use_sorted:
        order_by.reverse()
        for attr_or_field in order_by:
            # The field name can be prefixed by the minus sign and we need to
            # extract this information if we want to sort on simple object
            # attributes (non-model fields)
            if attr_or_field[0] == '-':
                reverse = True
                name = attr_or_field[1:]
            else:
                reverse = False
                name = attr_or_field

            queryset = sorted(queryset, key=attrgetter(name), reverse=reverse)
    else:
        queryset = queryset.order_by(*order_by)
        
    return queryset