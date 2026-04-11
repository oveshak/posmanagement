

from django.urls import path
from .views import (
    ActivityLogListView,
    AdminDashboardView,
    AreaDeleteView,
    AreaListView,
    BranchDeleteView,
    BranchListView,
    CustomLoginView,
    CustomerGroupDeleteView,
    CustomerGroupListView,
    DashboardView,
    LogoutView,
    ManagementDashboardView,
    MenuDeleteView,
    MenuListView,
    ProfilePageView,
    RoleCreateView,
    RoleDeleteView,
    RoleListView,
    RoleUpdateView,
    UserCreateView,
    UserDeleteView,
    UserListView,
    UserPasswordChangeView,
    UserUpdateView,
    ajax_areas_by_branch,
    ajax_area_meta,
    ajax_branch_meta,
    ajax_customer_groups,
    
    related_object_modal,
    menu_ajax_create,
    menu_json_detail,
    menu_ajax_update,
    test_widgets,
)


urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),

    path("", DashboardView.as_view(), name="dashboard"),
    path("dashboard/", DashboardView.as_view(), name="dashboard_page"),
    path("admin-dashboard/", AdminDashboardView.as_view(), name="admin_dashboard"),
    path("management/", ManagementDashboardView.as_view(), name="management_dashboard"),


    path("profile/", ProfilePageView.as_view(), name="profile_page"),
   
    path("change-password/", UserPasswordChangeView.as_view(), name="change_password"),

    path("users/", UserListView.as_view(), name="user_list"),
    path("users/create/", UserCreateView.as_view(), name="user_create"),
    path("users/<int:pk>/edit/", UserUpdateView.as_view(), name="user_update"),
    path("users/<int:pk>/delete/", UserDeleteView.as_view(), name="user_delete"),

    path("roles/", RoleListView.as_view(), name="role_list"),
    path("roles/create/", RoleCreateView.as_view(), name="role_create"),
    path("roles/<int:pk>/edit/", RoleUpdateView.as_view(), name="role_update"),
    path("roles/<int:pk>/delete/", RoleDeleteView.as_view(), name="role_delete"),

    path("branches/", BranchListView.as_view(), name="branch_list"),
    path("branches/<int:pk>/delete/", BranchDeleteView.as_view(), name="branch_delete"),

    path("areas/", AreaListView.as_view(), name="area_list"),
    path("areas/<int:pk>/delete/", AreaDeleteView.as_view(), name="area_delete"),

    path("customer-groups/", CustomerGroupListView.as_view(), name="customer_group_list"),
    path("customer-groups/<int:pk>/delete/", CustomerGroupDeleteView.as_view(), name="customer_group_delete"),

    path("menus/", MenuListView.as_view(), name="menu_list"),
    path("menus/<int:pk>/delete/", MenuDeleteView.as_view(), name="menu_delete"),

    path("activity-logs/", ActivityLogListView.as_view(), name="activity_logs"),
    path("test-widgets/", test_widgets, name="test_widgets"),

    # related modal routes
    path("ajax/related/<str:model_name>/create/", related_object_modal, name="related_object_create"),
    path("ajax/related/<str:model_name>/<int:pk>/edit/", related_object_modal, name="related_object_edit"),

    # optional old-compatible routes
    path("related-object-modal/<str:model_name>/", related_object_modal, name="related_object_create_legacy"),
    path("related-object-modal/<str:model_name>/<int:pk>/", related_object_modal, name="related_object_edit_legacy"),

    path("ajax/options/areas/", ajax_areas_by_branch, name="ajax_areas_by_branch"),
    path("ajax/options/customer-groups/", ajax_customer_groups, name="ajax_customer_groups"),
    path("ajax/meta/branch/<int:pk>/", ajax_branch_meta, name="ajax_branch_meta"),
    path("ajax/meta/area/<int:pk>/", ajax_area_meta, name="ajax_area_meta"),

    path("menu/ajax-create/", menu_ajax_create, name="menu_ajax_create"),
    path("menu/<int:pk>/json/", menu_json_detail, name="menu_json_detail"),
    path("menu/<int:pk>/ajax-update/", menu_ajax_update, name="menu_ajax_update"),
]


# from django.urls import path
# from .views import (
#     AdminDashboardView,
#     CustomLoginView,
#     DashboardView,
#     LogoutView,
#     ManagementDashboardView,
#     ProfilePageView,
#     UserPasswordChangeView,
#     load_areas,
#     load_customer_groups,

#     BranchListView, BranchCreateView, BranchUpdateView, BranchDeleteView,
#     AreaListView, AreaCreateView, AreaUpdateView, AreaDeleteView,
#     CustomerGroupListView, CustomerGroupCreateView, CustomerGroupUpdateView, CustomerGroupDeleteView,
#     UserListView, UserCreateView, UserUpdateView, UserDeleteView,
# )

# urlpatterns = [


#     path("login/", CustomLoginView.as_view(), name="login"),
#     path("logout/", LogoutView.as_view(), name="logout"),

#     path("", DashboardView.as_view(), name="dashboard"),
#     path("dashboard/", DashboardView.as_view(), name="dashboard_page"),
#     path("admin-dashboard/", AdminDashboardView.as_view(), name="admin_dashboard"),
#     path("management/", ManagementDashboardView.as_view(), name="management_dashboard"),


#     path("profile/", ProfilePageView.as_view(), name="profile_page"),
   
#     path("change-password/", UserPasswordChangeView.as_view(), name="change_password"),
#     # AJAX
#     path("ajax/load-areas/", load_areas, name="ajax_load_areas"),
#     path("ajax/load-customer-groups/", load_customer_groups, name="ajax_load_customer_groups"),

#     # Branch
#     path("branches/", BranchListView.as_view(), name="branch_list"),
#     path("branches/create/", BranchCreateView.as_view(), name="branch_create"),
#     path("branches/<int:pk>/edit/", BranchUpdateView.as_view(), name="branch_edit"),
#     path("branches/<int:pk>/delete/", BranchDeleteView.as_view(), name="branch_delete"),

#     # Area
#     path("areas/", AreaListView.as_view(), name="area_list"),
#     path("areas/create/", AreaCreateView.as_view(), name="area_create"),
#     path("areas/<int:pk>/edit/", AreaUpdateView.as_view(), name="area_edit"),
#     path("areas/<int:pk>/delete/", AreaDeleteView.as_view(), name="area_delete"),

#     # Customer Group
#     path("customer-groups/", CustomerGroupListView.as_view(), name="customer_group_list"),
#     path("customer-groups/create/", CustomerGroupCreateView.as_view(), name="customer_group_create"),
#     path("customer-groups/<int:pk>/edit/", CustomerGroupUpdateView.as_view(), name="customer_group_edit"),
#     path("customer-groups/<int:pk>/delete/", CustomerGroupDeleteView.as_view(), name="customer_group_delete"),

#     # Users
#     path("users/", UserListView.as_view(), name="user_list"),
#     path("users/create/", UserCreateView.as_view(), name="user_create"),
#     path("users/<int:pk>/edit/", UserUpdateView.as_view(), name="user_edit"),
#     path("users/<int:pk>/delete/", UserDeleteView.as_view(), name="user_delete"),
# ]