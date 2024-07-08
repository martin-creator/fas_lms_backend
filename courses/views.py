from django.shortcuts import render, get_object_or_404
from .models import LearningPath

def learning_path_detail(request, pk):
    learning_path = get_object_or_404(LearningPath, pk=pk)
    return render(request, 'courses/learning_path_detail.html', {'learning_path': learning_path})
