import uuid

from django.contrib.auth import get_user_model, forms
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods, require_GET
from django.utils.translation import gettext_lazy as _
from .models import UsersProfile
from .forms import UserProfileForm, UserForm, DeleteUserForm


User = get_user_model()


@require_http_methods(("GET", "POST"))
def user_register_view(request):
    register_form = forms.UserCreationForm(request.POST or None)
    if request.method == 'POST':
        if register_form.is_valid():
            register_form.save()

            return HttpResponseRedirect(reverse_lazy("login"))
    context = {
        'register_form':register_form,
    }
    return render(request, "users/register.html", context)


@require_GET
def user_detail_view(request, pk):
    user = get_object_or_404(User, id=pk)

    context = {
      "user": user
    }
    return render(request, "users/user_detail.html", context)


@require_GET
def user_list_view(request):
    users_list = User.objects.all()
    paginate_by = 10
    paginate_class = Paginator(users_list, paginate_by)
    page_number = request.GET.get('page')
    page_class = paginate_class.page(page_number or 1)

    context = {
        'users_list': users_list,
        'paginate': paginate_class,
        'page': page_class,
    }
    return render(request, 'users/user_list.html', context=context)


@require_http_methods(("GET", "POST"))
def user_save(user_form, user_profile_form):
    user = user_form.save()
    print(user_form.cleaned_data.get('password'))
    if user_form.cleaned_data.get('password'):
        user.set_password(user_form.cleaned_data['password'])
        user.save(update_fields=['password'])
    user_profile = user_profile_form.save(commit=False)
    user_profile.user = user
    user_profile.save()
    return user


@require_http_methods(("GET", "POST"))
def user_create_view(request):
    user_form = UserForm(request.POST or None)
    user_profile_form = UserProfileForm(request.POST or None)
    if request.method == 'POST':
        if user_form.is_valid() and user_profile_form.is_valid():
            user_save(user_form, user_profile_form)
            return HttpResponseRedirect(reverse_lazy("users:user-list"))

    context = {
        'user_form': user_form,
        'user_profile_form': user_profile_form,
    }
    return render(request, 'users/user_form.html', context=context)


@require_http_methods(("GET", "POST"))
def user_delete_view(request, pk):
    user = get_object_or_404(User, id=pk)
    user_profile = get_object_or_404(UsersProfile, user_id=pk)
    delete_user = DeleteUserForm(request.POST or None)
    if request.method == "POST" and 'user_delete':
        user_profile.delete()
        user.delete()
        return HttpResponseRedirect(reverse_lazy("users:user-list"))

    context = {
        'delete_user': delete_user,
        }

    return render(request, 'users/user_delete.html', context=context)


@require_http_methods(("GET", "POST"))
def user_update_view(request, pk):
    user = get_object_or_404(User.objects.select_related('auth_token'), id=pk)
    user_profile = get_object_or_404(UsersProfile.objects.select_related('user'), user_id=pk)
    edit_user = UserForm(instance=user)
    edit_user_profile = UserProfileForm(instance=user_profile)
    if request.method == 'POST':
        if 'edit_user' in request.POST and 'edit_user_profile' in request.POST:
            edit_user_profile = UserProfileForm(request.POST, instance=user_profile)
            edit_user = UserForm(request.POST, instance=user)
            if edit_user.is_valid() and edit_user_profile.is_valid():
                if edit_user.cleaned_data.get('password'):
                    user.set_password(edit_user.cleaned_data['password'])
                edit_user.save()
                edit_user_profile.save()

                return HttpResponseRedirect(reverse_lazy("users:user-list"))


    context = {
        'edit_user_profile': edit_user_profile,
        'edit_user': edit_user,
    }
    return render(request, 'users/user_form.html', context=context)
