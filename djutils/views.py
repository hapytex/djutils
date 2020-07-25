from django.views.generic.edit import FormMixin

class AuthoredView(LoginRequiredMixin):
    author_field = 'author'

    def form_valid(self, form):
        setattr(
            form.instance,
            self.author_field,
            self.request.user
        )
        super().form_valid(form)

class SecondFormMixin(FormMixin):
    prefix = 'form1'
    form2_class = None
    initial2 = {}
    prefix2 = 'form2'

    def get_context_data(self, **kwargs):
        """Insert the second form into the context dict."""
        if 'form2' not in kwargs:
            kwargs['form2'] = self.get_form2()
        return super().get_context_data(**kwargs)

    def get_form2(self, form2_class=None):
        """Return an instance of the second form to be used in this view."""
        if form2_class is None:
            form2_class = self.get_form2_class()
        return form2_class(**self.get_form2_kwargs())

    def get_form2_class(self):
        """Return the second form class to use."""
        return self.form2_class

    def get_form2_kwargs(self):
        """Return the keyword arguments for instantiating the second form."""
        kwargs = {
            'initial': self.get_initial2(),
            'prefix': self.get_prefix2(),
        }
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_initial2(self):
        """Return the initial data to use for the second form on this view."""
        return self.initial2.copy()

    def get_prefix2(self):
        """Return the prefix to use for the second form."""
        return self.prefix2
