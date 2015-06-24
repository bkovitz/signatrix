from source import Source, HasSource
from misc import trace, dd, isiterable, Multiple

def strip_sources(obj):
    if isinstance(obj, HasSource):
        return obj.without_source()
    elif type(obj) is str:
        return obj
    elif isiterable(obj):
        return list(strip_sources(o) for o in obj)
    else:
        return obj

def reduce_to_text(obj):
    if hasattr(obj, 'reduced_to_text'):
        return obj.reduced_to_text
    elif hasattr(obj, 'text'):
        return obj.text
    elif type(obj) is str:
        return obj
    elif isinstance(obj, Multiple):
        return Multiple(*(reduce_to_text(o) for o in obj))
    elif isiterable(obj):
        return list(reduce_to_text(o) for o in obj)
    else:
        return obj

