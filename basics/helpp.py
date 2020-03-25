import inspect as _inspect


def _help_aux(obj, attr_pred):
    attributes = {}
    properties = {}
    exception_properties = {}
    methods = {}
    class_methods = {}
    class_attrs = {}
    others = {}
    for attr in dir(obj):
        if not attr_pred(attr):
            continue
        attr_value = _inspect.getattr_static(obj, attr)
        if _inspect.ismemberdescriptor(attr_value) and not hasattr(obj, attr):
            # This happens for empty slots.
            continue
        try:
            value = getattr(obj, attr)
        except Exception as e:
            exception_properties[attr] = attr_value, e
            continue
        if _inspect.ismemberdescriptor(attr_value):
            attributes[attr] = value
        elif _inspect.isdatadescriptor(attr_value):
            properties[attr] = attr_value, value
        elif isinstance(attr_value, classmethod) or isinstance(attr_value, staticmethod):
            class_methods[attr] = attr_value
        elif _inspect.isfunction(attr_value):
            methods[attr] = attr_value
        else:
            if value is not attr_value:
                others[attr] = attr_value, value
            # If an attribute is in both the type and the instance it will be said to be a class attribute.
            if hasattr(type(obj), attr) and value is getattr(type(obj), attr):
                class_attrs[attr] = attr_value
            else:
                attributes[attr] = attr_value

    return dict(attributes=attributes,
                properties=properties,
                exception_properties=exception_properties,
                methods=methods,
                class_methods=class_methods,
                class_attrs=class_attrs,
                others=others)


def _help(obj, attr_pred):
    import pydoc
    attr_dict = _help_aux(obj, attr_pred)
    attributes = attr_dict['attributes']
    properties = attr_dict['properties']
    exception_properties = attr_dict['exception_properties']
    class_attrs = attr_dict['class_attrs']
    methods = attr_dict['methods']
    class_methods = attr_dict['class_methods']
    others = attr_dict['others']

    result = ''
    result += 'Help on {}:\n\n'.format(repr(obj))

    result += 'Attributes:\n'
    for name, value in sorted(attributes.items()):
        value_repr = '\n' + repr(value)
        value_repr = value_repr.replace('\n', '\n' + ' ' * 8)
        result += '    {:15} : {}{}\n\n'.format(name, type(value).__name__, value_repr)
    if not attributes:
        result += '    None\n\n'

    result += '\nProperties:\n'
    for name, (prop, value) in sorted(properties.items()):
        value_repr = '\n' + repr(value)
        value_repr = value_repr.replace('\n', '\n' + ' ' * 8)
        doc = _inspect.getdoc(prop)
        if doc is None:
            doc = ''
        else:
            doc = ('\n' + doc).replace('\n', '\n    # ')
        result += '    {:15} : {}{}{}\n\n'.format(name, type(value).__name__, doc, value_repr)
    if not properties:
        result += '    None\n\n'

    if exception_properties:
        result += '\nFailed properties:\n'
        for name, (prop, exception) in sorted(exception_properties.items()):
            exception_repr = '\n' + repr(exception)
            exception_repr = exception_repr.replace('\n', '\n' + ' ' * 8)
            doc = _inspect.getdoc(prop)
            if doc is None:
                doc = ''
            else:
                doc = ('\n' + doc).replace('\n', '\n    # ')
            result += '    {:15} : {}{}{}\n\n'.format(name, type(exception).__name__, doc, exception_repr)

    if class_attrs:
        result += '\nClass attributes:\n'
        for name, value in sorted(class_attrs.items()):
            value_repr = '\n' + repr(value)
            value_repr = value_repr.replace('\n', '\n' + ' ' * 8)
            result += '    {:15} : {}{}\n\n'.format(name, type(value).__name__, value_repr)

    result += '\nMethods:\n'
    for name, value in sorted(methods.items()):
        doc_lines = pydoc.render_doc(value, renderer=pydoc.plaintext).splitlines()[2:]
        doc = '\n    '.join(doc_lines)
        result += '    '
        result += doc
        result += '\n\n'
    if not methods:
        result += '    None\n\n'

    if class_methods:
        result += '\nClass methods:\n'
        for name, value in sorted(class_methods.items()):
            doc_lines = pydoc.render_doc(value.__func__, renderer=pydoc.plaintext).splitlines()[2:]
            doc = '\n    '.join(doc_lines)
            result += '    '
            result += doc
            result += '\n\n'

    if others:
        result += '\nOthers:\n    '
        result += '\n    '.join(sorted(others))

    return result


def helpp(obj):
    """
    Print user-friendly information about the objects attributes.
    """
    print(_help(obj, lambda name: not name.startswith('_')))


def helppp(obj):
    """
    Print user-friendly information about the objects attributes.

    Similar to `helpp` but also shows private attributes.
    """
    print(_help(obj, lambda name: not name.startswith('__')))


def helpppp(obj):
    """
    Print user-friendly information about the objects attributes.

    Similar to `helpp` but shows all attributes.
    """
    print(_help(obj, lambda name: True))
