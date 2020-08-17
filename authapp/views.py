import uuid

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView, UpdateView
from django.views.generic.detail import SingleObjectMixin
from django.db.models import Prefetch
from .forms import UserForm, UserProfileForm
from .models import UserProfile

class UserProfileView(DetailView):
    template_name = 'authapp/user_profile.html'
    model = UserProfile
    context_object_name = 'profile'
    slug_url_kwarg = 'username'
    slug_field = 'user__username'

    

@login_required
def profile_redirector(request):
    return redirect('authapp:profile', username=request.user.username)


class UserProfileUpdateView(UpdateView):
    template_name = 'authapp/edit_profile.html'
    form_class = UserForm
    form_class_2 = UserProfileForm

    def get_context_data(self, **kwargs):
        context = super(UserProfileUpdateView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(instance=self.request.user)
        if 'form2' not in context:
            context['form2'] = self.form_class_2(instance=self.request.user.profile)  # noqa
        return context

    def get(self, request, *args, **kwargs):
        super(UserProfileUpdateView, self).get(request, *args, **kwargs)
        self.object = self.get_object()
        form = self.form_class(instance=self.request.user)
        form2 = self.form_class_2(instance=self.request.user.profile)

        return self.render_to_response(self.get_context_data(
            form=form, form2=form2
        ))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.request.user)
        form2 = self.form_class_2(request.POST, request.FILES,
                                  instance=self.request.user.profile)

        if form.is_valid() and form2.is_valid():
            form.save()
            data = form2.save(commit=False)
            if request.FILES.get('avatar', None):
                data.avatar = request.FILES['avatar']
                data.avatar.name = '{0}_p.jpg'.format(str(uuid.uuid4()))
            data.save()
            return redirect('authapp:user_profile')
        else:
            return self.render_to_response(
                self.get_context_data(form=form, form2=form2)
                )

    def get_object(self, queryset=None):
        return self.request.user
