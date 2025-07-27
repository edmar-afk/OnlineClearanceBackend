from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('programs/', views.ProgramsListAPIView.as_view(), name='programs-list'),
    path('register/', views.RegisterUserAPIView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('user/<int:user_id>/', views.GetUserByIdView.as_view(), name='get_user_by_id'),
    path('upload-signature/', views.SignatureUploadView.as_view(), name='upload-signature'),
    
    path('signature/<int:staff_id>/', views.SignatureDetailView.as_view()),
    
    path('student/<int:user_id>/', views.StudentDetailByUserIdView.as_view(), name='student-detail-by-user-id'),
    
    path('clearances/', views.ClearanceListView.as_view(), name='clearance-list'),
    path('clearances/create/', views.ClearanceCreateView.as_view(), name='create-clearance'),
    path('clearance/latest/', views.LatestClearanceView.as_view(), name='latest-clearance'),
    path('clearances/<int:id>/', views.ClearanceDetailView.as_view(), name='clearance-detail'),
    path('student-clearance/request-latest/', views.RequestLatestClearanceView.as_view(), name='request-latest-clearance'),
    path('student-clearance/<int:student_id>/', views.StudentClearanceByStudentView.as_view(), name='student-clearance-by-student'),
    path('student-clearances/', views.StudentClearanceListView.as_view(), name='student-clearance-list'),
    path("student-clearances/<int:pk>/update-status/", views.UpdateStudentClearanceStatus.as_view(), name="update-student-clearance-status"),
    path('students/count/', views.StudentCountView.as_view(), name='student-count'),
    
    path('clearance-signatures/', views.ClearanceSignatureListView.as_view(), name='clearance-signatures'),
    path('clearance-signatures/create/<int:student_id>/<int:program_id>/', views.ClearanceSignatureCreateView.as_view(), name='create-clearance-signature'),
    path('clearance-signatures/status/<int:student_id>/<int:program_id>/', views.GetClearanceSignatureView.as_view(), name='get-clearance-signature'),
    path('clearance-signatures/<int:signature_id>/update-status/', views.UpdateClearanceSignatureStatusView.as_view()),
    path(
    'clearance-signatures/<str:program_name>/<str:last_name>/<str:year_level>/',
    views.ClearanceSignatureByParamsView.as_view(),
    name='clearance-signatures-by-params'
)

]
