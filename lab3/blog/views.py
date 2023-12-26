from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.template.context_processors import request
from django.views import generic

from . import forms
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from .models import Profile, Blog, BlogComment
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

def index(request):
    blog = Blog.objects.all()
    return render(request, 'index.html', {"blog":blog})

class BlogDetailView(generic.DetailView):
    template_name = 'blog.html'
    model = Blog


class BlogListbyAuthorView(generic.ListView):
    model = Blog
    paginate_by = 5
    template_name ='author.html'

    def get_queryset(self):
        id = self.kwargs['pk']
        target_author=get_object_or_404(User, pk = id)
        return Blog.objects.filter(author=target_author)

    def get_context_data(self, **kwargs):
        context = super(BlogListbyAuthorView, self).get_context_data(**kwargs)
        context['blogger'] = get_object_or_404(User, pk = self.kwargs['pk'])
        return context



class BlogCommentCreate(LoginRequiredMixin, CreateView):
    model = BlogComment
    fields = ['description',]
    template_name = 'comment.html'

    def get_context_data(self, **kwargs):
        context = super(BlogCommentCreate, self).get_context_data(**kwargs)
        context['blog'] = get_object_or_404(Blog, pk = self.kwargs['pk'])
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.blog=get_object_or_404(Blog, pk = self.kwargs['pk'])
        return super(BlogCommentCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('blog-detail', kwargs={'pk': self.kwargs['pk'],})






class RegisterUserView(CreateView):
    model = User
    form_class = forms.RegisterUserForm
    template_name = "register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        # Save the user object without committing to the database
        user = form.save(commit=False)
        # Set the user's password
        user.set_password(form.cleaned_data.get('password'))
        user.save()

        # Create a profile for the user
        Profile.objects.create(user=user)

        return super().form_valid(form)

class LoginUserView(LoginView):
    template_name = "login.html"

def logout_view(request):
    logout(request)
    return redirect("login")

# class CreatePost(CreateView):
#     model = Blog
#     form_class = forms.CreateBlogPost
#     template_name = "create_blog.html"
#     success_url = reverse_lazy("home")
#
#     def form_valid(self, form):
#         post = form.save()
#         print(post)
#         Blog.objects.create(name=post, author=request.user.Profile)
#         return super().form_valid(form)

def CreatePost(request):
    if request.method == 'POST':
        form = forms.CreateBlogPost(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')  # Перенаправляем на страницу со списком постов
    else:
        form = forms.CreateBlogPost()
    return render(request, 'create_blog.html', {'form': form})




@login_required()
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Ваш аккаунт был обновлен!')
            return redirect('profile')

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'profile.html', context)