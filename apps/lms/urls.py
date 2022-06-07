from django.urls import path

from .views import LessonDetailsView, LessonCreateView, TeacherClassesView, TeacherListView

app_name = 'lms'

urlpatterns = [
    path('', TeacherListView.as_view(), name='teachers-list'),
    path('<int:teacher_id>/', TeacherClassesView.as_view(), name='teacher-classes'),
    path('lesson/<int:lesson_id>/', LessonDetailsView.as_view(), name='lesson-details'),
    path('class/<int:class_id>/lesson/add/', LessonCreateView.as_view(), name='lesson-create')
]