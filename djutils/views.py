class AuthoredView(LoginRequiredMixin):
    author_field = 'author'

    def form_valid(self, form):
        setattr(
            form.instance,
            self.author_field,
            self.request.user
        )
        super().form_valid(form)
