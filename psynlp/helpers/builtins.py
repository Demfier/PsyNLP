import builtins as __builtin__


def init_verbose(verbose=False):
    if not verbose:
        __builtin__.verbose_print_1 = lambda *a, **k: None
        __builtin__.verbose_print_2 = lambda *a, **k: None
        __builtin__.verbose_print_3 = lambda *a, **k: None
    elif verbose == 1:
        __builtin__.verbose_print_1 = print
        __builtin__.verbose_print_2 = lambda *a, **k: None
        __builtin__.verbose_print_3 = lambda *a, **k: None
    elif verbose == 2:
        __builtin__.verbose_print_1 = print
        __builtin__.verbose_print_2 = print
        __builtin__.verbose_print_3 = lambda *a, **k: None
    else:
        __builtin__.verbose_print_1 = print
        __builtin__.verbose_print_2 = print
        __builtin__.verbose_print_3 = print
