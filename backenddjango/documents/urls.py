from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'documents', views.DocumentViewSet, basename='document')
router.register(r'notes', views.NoteViewSet, basename='note')
router.register(r'fees', views.FeeViewSet, basename='fee')
router.register(r'repayments', views.RepaymentViewSet, basename='repayment')
router.register(r'note-comments', views.NoteCommentViewSet, basename='note-comment')

urlpatterns = router.urls + [
    path('documents/<int:pk>/create-version/', views.DocumentCreateVersionView.as_view(), name='document-create-version'),
    path('fees/<int:pk>/mark-paid/', views.FeeMarkPaidView.as_view(), name='fee-mark-paid'),
    path('repayments/<int:pk>/mark-paid/', views.RepaymentMarkPaidView.as_view(), name='repayment-mark-paid'),
    path('applications/<int:application_id>/ledger/', views.ApplicationLedgerView.as_view(), name='application-ledger'),
]
