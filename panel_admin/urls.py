from django.urls import path
from .views import *

app_name = "panel_admin"

urlpatterns = [
    path('', AdminDashboardView.as_view(), name='admin_dashboard'),

    # Eventos
    path('events/', EventListView.as_view(), name='events_list'),
    path('events/add/', EventCreateView.as_view(), name='event_add'),
    path('events/<int:pk>/edit/', EventUpdateView.as_view(), name='event_edit'),
    path('events/<int:pk>/delete/', EventDeleteView.as_view(), name='event_delete'),

    # Categorías
    path('categories/', CategoryListView.as_view(), name='categories_list'),
    path('categories/add/', CategoryCreateView.as_view(), name='category_add'),
    path('categories/<int:pk>/edit/', CategoryUpdateView.as_view(), name='category_edit'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),

    # Lugares
    path('venues/', VenueListView.as_view(), name='venues_list'),
    path('venues/add/', VenueCreateView.as_view(), name='venue_add'),
    path('venues/<int:pk>/edit/', VenueUpdateView.as_view(), name='venue_edit'),
    path('venues/<int:pk>/delete/', VenueDeleteView.as_view(), name='venue_delete'),

    # Comentarios
    path('comments/', CommentListView.as_view(), name='comments_list'),
    path('comments/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),

    # Tickets
    path('tickets/<int:pk>/edit/', TicketUpdateView.as_view(), name='ticket_edit'),
    path('tickets/<int:pk>/delete/', TicketDeleteView.as_view(), name='ticket_delete'),

    # Reembolsos
    path('refunds/', RefundRequestListView.as_view(), name='refunds_list'),
    path('refunds/<int:pk>/update/', RefundRequestUpdateView.as_view(), name='refund_update'),

    # Notificaciones
    path('notifications/', NotificationListView.as_view(), name='notifications_list'),
    path('notifications/add/', NotificationCreateView.as_view(), name='notification_add'),
    path('notifications/<int:pk>/edit/', NotificationUpdateView.as_view(), name='notification_edit'),
    path('notifications/<int:pk>/delete/', NotificationDeleteView.as_view(), name='notification_delete'),
]
