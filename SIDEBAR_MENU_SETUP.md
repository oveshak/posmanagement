# 🎯 Role-wise Sidebar Menu System - Setup Guide

## ✅ What's New

A complete **dynamic, role-based sidebar menu system** that shows different menus based on user roles.

### Features:
✅ **Dynamic Menu Display** - Menus shown based on user roles  
✅ **Hierarchical Menus** - Support for main menus and submenus  
✅ **Admin Controls** - Manage menus in Django admin  
✅ **Responsive** - Works on mobile and desktop  
✅ **Font Awesome Icons** - Beautiful icon support  
✅ **Easy to Customize** - Simple menu model with fields for icons and URLs  

---

## 🚀 Setup Steps

### 1️⃣ **Create and Run Migrations**

```bash
# Generate migration for new Menu model
python manage.py makemigrations

# Apply migration
python manage.py migrate
```

### 2️⃣ **Create Menu Items in Admin**

Go to `/admin/` and navigate to **Menus**:

**Example Menu Structure:**

```
Dashboard (parent: None)
├── icon: fas fa-chart-line
├── url: dashboard
├── order: 0

Users (parent: None)
├── icon: fas fa-users
├── url: user_list
├── order: 1

Users > Create User (parent: Users)
├── icon: fas fa-user-plus
├── url: user_create
├── order: 1

Roles (parent: None)
├── icon: fas fa-crown
├── url: role_list
├── order: 2

Activity Logs (parent: None)
├── icon: fas fa-history
├── url: activity_logs
├── order: 3
```

### 3️⃣ **Create Roles and Assign Menus**

Go to `/admin/` → **Roles**:

**Example Role: Editor**
- Name: `Editor`
- Description: `Can view and edit content`
- Menu Items (select multiple):
  - ☑️ Dashboard
  - ☑️ Posts
  - ☑️ Comments

**Example Role: Manager**
- Name: `Manager`
- Description: `Full management access`
- Menu Items (select multiple):
  - ☑️ Dashboard
  - ☑️ Users
  - ☑️ Users > Create User
  - ☑️ Roles
  - ☑️ Activity Logs

### 4️⃣ **Assign Roles to Users**

Go to `/admin/` → **Users** → Edit User:

**Example Assignments:**
- `john@example.com` → Manager role
- `editor@example.com` → Editor role

---

## 📊 Menu Model Fields

```python
class Menu(models.Model):
    name          # Menu display name
    icon          # Font Awesome icon (e.g., "fas fa-dashboard")
    url           # Django URL name or path
    order         # Display order (0, 1, 2, etc.)
    is_active     # Toggle visibility
    description   # Optional description
    parent        # NULL = main menu, or link to parent menu
    created_at    # Auto timestamp
    updated_at    # Auto timestamp
```

---

## 🎨 How It Works

1. **User logs in**
2. **Context processor (`user_menus_context`)** runs:
   - Gets all user's assigned roles
   - Collects all menus for those roles
   - Creates menu hierarchy (main + submenus)
3. **Sidebar template** displays menus
4. **Different users see different menus** based on their roles

---

## 📁 Files Created/Updated

### New Files:
- ✅ `user/models.py` - Added `Menu` model
- ✅ `user/context_processors.py` - Menu context processor
- ✅ `templates/common/sidebar_dynamic.html` - New dynamic sidebar
- ✅ `templates/dashboard_layout.html` - New dashboard layout
- ✅ `user/templatetags/custom_filters.py` - Dictionary lookup filter
- ✅ `user/templatetags/__init__.py` - Template tags package

### Updated Files:
- ✅ `user/models.py` - Changed `Roles.menu` from `Group` to `Menu`
- ✅ `managements/settings.py` - Added context processor
- ✅ `user/admin.py` - Added `MenuAdmin`
- ✅ `user/forms.py` - Updated `RoleForm` with description field

---

## 🧪 Testing

### Test 1: Create Sample Data

```python
# In Django shell: python manage.py shell

from user.models import Menu, Roles, Users

# Create dashboard menu
Menu.objects.create(
    name="Dashboard",
    icon="fas fa-chart-line",
    url="dashboard",
    order=0
)

# Create users menu
users_menu = Menu.objects.create(
    name="Users",
    icon="fas fa-users",
    url="user_list",
    order=1
)

# Create Editor role
editor_role = Roles.objects.create(
    name="Editor",
    description="Content editor"
)
editor_role.menu.add(Menu.objects.get(name="Dashboard"))

# Assign role to user
user = Users.objects.get(email="user@example.com")
user.roles.add(editor_role)
```

### Test 2: Visual Check

1. Login as admin: http://127.0.0.1:8000/user/login/
2. You should see the sidebar with all menus (admins see all)
3. Create a regular user with an Editor role
4. Login as that user
5. Sidebar shows only Dashboard menu (assigned to Editor role)

### Test 3: Dynamic Submenus

1. In admin, create submenu:
   - Name: "Create Post"
   - parent: Users menu
   - icon: "fas fa-file-plus"
   - url: "post_create"

2. Refresh page - submenu appears under Users

---

## 🔐 Security Notes

✅ **Admins/Staff** see all active menus  
✅ **Regular users** see only menus assigned to their roles  
✅ **Anonymous users** see no menus (redirected to login)  
✅ **Permission checks** should be in views (this sidebar is UI only)

---

## 🎯 Next Steps

### To Use New Layout in Your Templates:

**OLD:** `{% extends 'base.html' %}`  
**NEW:** `{% extends 'dashboard_layout.html' %}`

Or better yet, use the new layout everywhere for consistent sidebar!

### To Add Font Awesome Icons:

```html
<i class="fas fa-icon-name"></i>
```

Visit: https://fontawesome.com/search to find icons

---

## 📝 Available Menus Created by Default

After migration, create these sample menus:

| Menu Name | Icon | URL | Order | Parent |
|-----------|------|-----|-------|--------|
| Dashboard | fas fa-chart-line | dashboard | 0 | None |
| Users | fas fa-users | user_list | 1 | None |
| Create User | fas fa-user-plus | user_create | 1 | Users |
| Edit User | fas fa-user-edit | user_update | 2 | Users |
| Roles | fas fa-crown | role_list | 2 | None |
| Activity Logs | fas fa-history | activity_logs | 3 | None |
| Settings | fas fa-cog | settings | 4 | None |

---

## 🆘 Troubleshooting

**Q: Sidebar doesn't show?**
- Verify `user_menus_context` is in `TEMPLATES['OPTIONS']['context_processors']`
- Check user has roles assigned
- Check roles have menus assigned

**Q: Menus not in right order?**
- Update the `order` field in admin
- Saves should reflect immediately

**Q: Submenus not showing?**
- Set the `parent` field to the main menu
- Make sure submenu is active (`is_active=True`)
- Both parent and submenu should be assigned to role

**Q: Icons not displaying?**
- Verify Font Awesome CDN link in templates
- Check icon name is correct (e.g., `fas fa-dashboard` not `dashboard`)
- Console errors? Check browser developer tools (F12)

---

## 📚 Additional Resources

- Font Awesome Icons: https://fontawesome.com/search
- Django Context Processors: https://docs.djangoproject.com/en/stable/ref/templates/api/#django.template.context_processors
- Template Filters: https://docs.djangoproject.com/en/stable/ref/templates/builtins/#std-templatefilter-default

---

✅ **Setup Complete!** Your role-wise sidebar menu system is ready to use.
