from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from tasks import models
from django.views.generic import ListView, DetailView, CreateView, View, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from tasks.mixins import UserIsOwnerMixin
from tasks.forms import TaskForm, TaskFilterForm, CommentForm
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import InterestingPost, InterestingComments, InterestingLikes, InterestingPostLike, Task
from .forms import InterestingPostForm, InteresstingCommentForm 


class TaskListView(ListView):
    model = models.Task
    context_object_name = "tasks"
    template_name = "tasks/task_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get("status", "")
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = TaskFilterForm(self.request.GET)
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = models.Task
    context_object_name = "task"
    template_name = 'tasks/task_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()  # Додаємо порожню форму коментаря в контекст
        return context

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.task = self.get_object()
            comment.save()
            return redirect('tasks:task-detail', pk=comment.task.pk)
        else:
            # Тут можна обробити випадок з невалідною формою
            pass


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = models.Task
    template_name = "tasks/task_form.html"
    form_class = TaskForm
    success_url = reverse_lazy("tasks:task-list")

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class TaskCompleteView(LoginRequiredMixin, UserIsOwnerMixin, View):
    def post(self, request, *args, **kwargs):
        task = self.get_object()
        task.status = "done"
        task.save()
        return HttpResponseRedirect(reverse_lazy("tasks:task-list"))

    def get_object(self):
        task_id = self.kwargs.get("pk")
        return get_object_or_404(models.Task, pk=task_id)


class TaskUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = models.Task
    form_class = TaskForm
    template_name = "tasks/task_update_form.html"
    success_url = reverse_lazy("tasks:task-list")


class TaskDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = models.Task
    success_url = reverse_lazy("tasks:task-list")
    template_name = "tasks/task_delete_confirmation.html"


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Comment
    fields = ['content']
    template_name = 'tasks/edit_comment.html'

    def form_valid(self, form):
        comment = self.get_object()
        if comment.author != self.request.user:
            raise PermissionDenied("Ви не можете редагувати цей коментар.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('tasks:task_detail', kwargs={'pk': self.object.task.pk})


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Comment
    template_name = 'tasks/delete_comment.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)

    def get_success_url(self):
        return reverse_lazy('tasks:task_detail', kwargs={'pk': self.object.task.pk})


class CommentLikeToggle(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(models.Comment, pk=self.kwargs.get('pk'))
        like_qs = models.Like.objects.filter(comment=comment, user=request.user)
        if like_qs.exists():
            like_qs.delete()
        else:
            models.Like.objects.create(comment=comment, user=request.user)
        return HttpResponseRedirect(comment.get_absolute_url())


class CustomLoginView(LoginView):
    template_name = "tasks/login.html"
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = "tasks:login"


class RegisterView(CreateView):
    template_name = "tasks/register.html"
    form_class = UserCreationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(reverse_lazy("tasks:login"))

class InterestingPostListView(ListView):
    model = InterestingPost
    template_name = 'interesting/post_list.html'   # Указываем нужный шаблон
    context_object_name = 'posts'
    ordering = ['-created_at']

class InterestingPostDetailView(LoginRequiredMixin, DetailView):
    model = InterestingPost
    template_name = 'interesting/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = InteresstingCommentForm()
        return context
    
    def post(self, request, *args, **kwargs):
        comment_form = InteresstingCommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = self.get_object()
            comment.save()
            return redirect('tasks:post-detail', pk=comment.post.pk)
        else:
            context = self.get_context_data()
            context['comment_form'] = comment_form
            return self.render_to_response(context)
        
class InterestingPostCreateView(LoginRequiredMixin, CreateView):
    model = InterestingPost
    form_class = InterestingPostForm
    template_name = 'interesting/post_form.html'
    success_url = reverse_lazy('tasks:post-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class InterestingPostUpdateView(LoginRequiredMixin, UpdateView):
    model = InterestingPost
    form_class = InterestingPostForm
    template_name = 'interesting/post_form.html'
    success_url = reverse_lazy('interesting:post-list')

class InterestingPostDeleteView(LoginRequiredMixin, DeleteView):
    model = InterestingPost
    template_name = 'interesting/post_delete_confirmation.html'
    success_url = reverse_lazy('inteersting:post-list')

class InterestingCommentUpdateView(LoginRequiredMixin, UpdateView):
    model = InterestingPost
    fields = ['content', 'media']
    template_name = 'interessting/comment_update_form.html'

    def get_success_url(self):
        return reverse_lazy('interesting:post-detail', kwargs={'pk': self.object.post.pk})
    
class InterestingLikeToggle(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(InterestingComments, pk=self.kwargs.get('pk'))
        like_qs = InterestingLikes.objects.filter(comment=comment, user=request.user)
        if like_qs.exists():
            like_qs.delete()
        else:
            InterestingLikes.objects.create(comment=comment, user=request.user)
        return redirect(comment.get_absolute_url())
    
class InterestingPostLikeToggleView(LoginRequiredMixin, View):
    def post(self, request, pk):
        post = get_object_or_404(InterestingPost, pk=pk)
        like_qs = InterestingPostLike.objects.filter(post=post, user=request.user)
        if like_qs.exists():
            like_qs.delete()  # Если лайк уже поставлен, удаляем его
        else:
            InterestingPostLike.objects.create(post=post, user=request.user)
        # Перенаправляем пользователя, например, на детальную страницу поста
        return redirect('tasks:post-list')
    
class TaskLikeToggleView(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        # Если пользователь уже поставил лайк, убираем его, иначе – добавляем
        if request.user in task.likes.all():
            task.likes.remove(request.user)
        else:
            task.likes.add(request.user)
        # Перенаправляем пользователя обратно на ту же страницу
        return redirect(request.META.get('HTTP_REFERER', task.get_absolute_url()))