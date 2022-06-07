from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView

from apps.lms.models import Group, Lesson

User = get_user_model()


class TeacherListView(ListView):
    model = User
    template_name = 'lms/teachers_list.html'

    def get_queryset(self):
        return super().get_queryset().filter(is_teacher=True)


class TeacherClassesView(LoginRequiredMixin, ListView):
    template_name = 'lms/teachers_classes.html'
    model = Group

    def get_queryset(self):
        teacher_id = self.kwargs.get('teacher_id')
        return super().get_queryset().filter(teacher_id=teacher_id)


class LessonDetailsView(LoginRequiredMixin, DetailView):
    model = Lesson
    pk_url_kwarg = 'lesson_id'
    template_name = 'lms/lesson_details.html'


class LessonCreateView(CreateView):
    model = Lesson
    fields = ['name', 'date', 'description']
    template_name = 'lms/lesson_create.html'

    def dispatch(self, request, *args, **kwargs):
        self.group = get_object_or_404(Group, id=kwargs.get('class_id'))
        return super(LessonCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        result = super(LessonCreateView, self).form_valid(form)
        self.object.group = self.group
        self.object.save()
        return result

    def get_success_url(self):
        return reverse_lazy('lms:lesson-details', kwargs={'lesson_id': self.object.id})
