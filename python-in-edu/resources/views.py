from django.views import generic
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect


from .models import Profile, Resource
from . import choices


class ResourceDetailView(generic.DetailView):
    model = Resource
    template_name = 'resources/resource_detail.html'


class ResourceListView(generic.ListView):
    model = Resource
    template_name = 'resources/resource_list.html'

    def get_context_data(self, **kwargs):
        # overrides default to get only accepted resources
        context = super().get_context_data(**kwargs)
        context['resource_list'] = Resource.objects.filter(status=choices.ResourceStatusChoices.ACCEPTED)
        return context


class ResourceCreateView(LoginRequiredMixin, generic.CreateView):
    model = Resource
    fields = ['title', 'url', 'requires_signup', 'resource_type', 'audience',
        'devices', 'language', 'requirements', 'description', 'attribution',
        'author_bio', 'organization', 'contact', 'standards', 'license']
    template_name = "resources/add_resource.html"

    def get_success_url(self, instance):
        return reverse('resource_detail', kwargs={'pk': instance.pk })

    def form_valid(self, form):
        unsaved_resource_instance = form.save(commit=False)
        unsaved_resource_instance.submitter = self.request.user
        unsaved_resource_instance.save()
        return HttpResponseRedirect(self.get_success_url(instance=unsaved_resource_instance))


class ResourceUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Resource
    fields = ['title', 'requires_signup', 'resource_type', 'audience',
        'devices', 'language', 'requirements', 'description', 'attribution',
        'author_bio', 'organization', 'contact', 'standards']
    template_name = 'resources/update_resource.html'

    def get_success_url(self):
        return reverse('resource_detail', kwargs={'pk': self.object.pk })


class ProfileDetailView(generic.DetailView):
    model = Profile
    template_name = 'resources/profile_detail.html'

    def get_object(self, queryset=None):
        username = self.kwargs.get('username', None)
        user = get_object_or_404(User, username=username)
        return user.profile


class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Profile
    fields = ['organization', 'country', 'roles', 'populations', 'underrep', 'psf_member']
    template_name = 'resources/profile_update.html'

    def get_object(self, queryset=None):
        username = self.kwargs.get('username', None)
        user = get_object_or_404(User, username=username)
        return user.profile

    def get_success_url(self):
        return reverse('profile_detail', kwargs={'username': self.request.user.username })


class ProfileListView(generic.ListView):
    model = Profile
    template_name = 'resources/profile_list.html'

