"""
A package that contains useful models and managers for Django models.
"""

from django.db.models import Manager, QuerySet


# pylint: disable=too-few-public-methods
class PreprocessManager(Manager):
    '''
    A manager that can be used to each time perform a certain
    operation on the QuerySet when we access it, for example
    annotating or filtering the queryset.

    This function is used as a superclass for some managers.
    using this manager itself will fail.
    '''

    _qsfunction = None

    def __init__(self, *args, **kwargs):
        '''
        Initializes the PreprocessManager with an arbitrary
        number of positional and named arguments that are each
        time passed to the relevant function of the QuerySet
        behind the manager.
        '''
        super(PreprocessManager, self).__init__()
        self._prcargs = args
        self._prckwargs = kwargs

    def _process_qs(self, queryset):
        # pylint: disable=not-callable
        return type(self)._qsfunction(
            queryset,
            *self._prcargs,
            **self._prckwargs
        )

    def get_queryset(self):
        '''
        Overrides the get_queryset function to process the
        QuerySet before passing it to the caller of the
        manager.
        '''
        return self._process_qs(
            super(
                PreprocessManager,
                self
            ).get_queryset()
        )


class AnnotatedManager(PreprocessManager):
    '''
    A manager that automatically annotates the queryset
    with the given annotations in the constructor of the
    AnnotatedManager.
    '''
    _qsfunction = QuerySet.annotate


class FilteredManager(PreprocessManager):
    '''
    A manager that automatically filters the queryset
    with the given filters in the constructor of the
    FilteredManager.
    '''
    _qsfunction = QuerySet.filter
