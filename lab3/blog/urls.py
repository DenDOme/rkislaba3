from django.urls import path, include
from . import views


urlpatterns = [
    path('blog/', views.index, name="home"),
    path('login/', views.LoginUserView.as_view(), name="login"),
    path('register/', views.RegisterUserView.as_view(), name="register"),
    path('logout/', views.logout_view, name="logout"),
    path('profile/', views.profile, name="profile"),
    path('create/', views.CreatePost, name="create"),
    path('blog/<int:pk>/comment/', views.BlogCommentCreate.as_view(), name='blog_comment'),
    path('blogger/<int:pk>', views.BlogListbyAuthorView.as_view(), name='blog_author'),
    path('blog/<int:pk>', views.BlogDetailView.as_view(), name='blog-detail'),
]