from django import forms
from tasks.models import Task, Comment, InterestingPost, InterestingComments


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "status", "priority", "due_date", "image"]

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

        self.fields["due_date"].widget.attrs["class"] += " my-custom-datepicker"


class TaskFilterForm(forms.Form):
    STATUS_CHOICES = [
        ("", "Всі"),
        ("todo", "To Do"),
        ("in_progress", "In Progress"),
        ("done", "Done"),
    ]
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False, label="Статус")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Меняем класс на form-select (Bootstrap) + свои стили
        self.fields["status"].widget.attrs.update({
            "class": "form-select custom-dark-select"
        })




class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'media']
        widgets = {
            "media": forms.FileInput()
        }

class InterestingPostForm(forms.ModelForm):
    class Meta:
        model = InterestingPost
        fields = ['title', 'content', 'image']

class InteresstingCommentForm(forms.ModelForm):
    class Meta:
        model = InterestingComments
        fields = ['content', 'media']

