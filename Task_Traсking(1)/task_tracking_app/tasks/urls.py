from django.urls import path
from tasks import views
from .views import (
    InterestingPostListView,
    InterestingPostDetailView,
    InterestingPostCreateView,
    InterestingPostUpdateView,
    InterestingPostDeleteView,
    InterestingCommentUpdateView, 
    InterestingLikeToggle, 
    InterestingPostLikeToggleView,
    TaskLikeToggleView
)

urlpatterns = [
    # URL'ы для задач
    path("", views.TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk>/", views.TaskDetailView.as_view(), name="task-detail"),
    path("tasks/<int:pk>/update/", views.TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete/", views.TaskDeleteView.as_view(), name="task-delete"),
    path("tasks/task-create/", views.TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/complete/", views.TaskCompleteView.as_view(), name="task-complete"),
    path("tasks/comment/edit/<int:pk>/", views.CommentUpdateView.as_view(), name="edit_comment"),
    path("tasks/comment/delete/<int:pk>/", views.CommentDeleteView.as_view(), name="delete_comment"),
    path("tasks/comment/like/<int:pk>/", views.CommentLikeToggle.as_view(), name="comment-like-toggle"),
    path("tasks/login/", views.CustomLoginView.as_view(), name="login"),
    path("tasks/logout/", views.CustomLogoutView.as_view(), name="logout"),
    path("tasks/register/", views.RegisterView.as_view(), name="register"),
    path("tasks/<int:pk>/like/", TaskLikeToggleView.as_view(), name="like-task"),

    # URL'ы для "цікаве Інфо"
    path("interesting/", InterestingPostListView.as_view(), name="post-list"),
    path("interesting/<int:pk>/", InterestingPostDetailView.as_view(), name="post-detail"),
    path("interesting/create/", InterestingPostCreateView.as_view(), name="post-create"),
    path("interesting/<int:pk>/update/", InterestingPostUpdateView.as_view(), name="post-update"),
    path("interesting/<int:pk>/delete/", InterestingPostDeleteView.as_view(), name="post-delete"),
    path("interesting/comment/<int:pk>/update/", InterestingCommentUpdateView.as_view(), name="comment-update"),
    path("interesting/comment/<int:pk>/like/", InterestingLikeToggle.as_view(), name="comment-like"),
    path('interesting/<int:pk>/like/', InterestingPostLikeToggleView.as_view(), name='post-like'),
    
]

app_name = "tasks"

