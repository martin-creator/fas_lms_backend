from .views import learning_path_detail

urlpatterns = [
    # ... other paths ...
    path('learning-path/<int:pk>/', learning_path_detail, name='learning_path_detail'),
]
