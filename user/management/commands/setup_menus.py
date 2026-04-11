from django.core.management.base import BaseCommand
from user.models import Menu, Roles


class Command(BaseCommand):
    help = 'Setup sample menus and roles for testing'

    def handle(self, *args, **options):
        self.stdout.write("🔧 Setting up sample menus...\n")

        # Create sample menus
        menus = [
            {
                'name': 'Dashboard',
                'icon': 'fas fa-chart-line',
                'url': 'dashboard',
                'order': 0,
                'parent': None,
                'is_active': True,
            },
            {
                'name': 'User Management',
                'icon': 'fas fa-users',
                'url': 'management_dashboard',
                'order': 1,
                'parent': None,
                'is_active': True,
            },
            {
                'name': 'Create User',
                'icon': 'fas fa-user-plus',
                'url': 'user_create',
                'order': 1,
                'parent': 'User Management',
                'is_active': True,
            },
            {
                'name': 'View Users',
                'icon': 'fas fa-list',
                'url': 'user_list',
                'order': 2,
                'parent': 'User Management',
                'is_active': True,
            },
            {
                'name': 'Roles & Permissions',
                'icon': 'fas fa-crown',
                'url': 'role_list',
                'order': 2,
                'parent': None,
                'is_active': True,
            },
            {
                'name': 'Activity Logs',
                'icon': 'fas fa-history',
                'url': 'activity_logs',
                'order': 3,
                'parent': None,
                'is_active': True,
            },
        ]

        created_menus = {}
        for menu_data in menus:
            parent = menu_data.pop('parent')
            parent_obj = None
            
            if parent:
                parent_obj = created_menus.get(parent)
            
            menu, created = Menu.objects.get_or_create(
                name=menu_data['name'],
                defaults={**menu_data, 'parent': parent_obj}
            )
            
            created_menus[menu_data['name']] = menu
            
            status = "✅ Created" if created else "⏭️  Already exists"
            self.stdout.write(f"{status}: {menu.name}")

        # Create sample roles
        self.stdout.write("\n🔧 Setting up sample roles...\n")

        # Editor role
        editor_role, created = Roles.objects.get_or_create(
            name='Editor',
            defaults={'description': 'Content editor with limited access'}
        )
        if created:
            editor_role.menu.add(
                created_menus['Dashboard'],
            )
            self.stdout.write("✅ Created: Editor role (Dashboard only)")
        else:
            self.stdout.write("⏭️ Already exists: Editor role")

        # Manager role
        manager_role, created = Roles.objects.get_or_create(
            name='Manager',
            defaults={'description': 'Full management access'}
        )
        if created:
            manager_role.menu.add(
                created_menus['Dashboard'],
                created_menus['User Management'],
                created_menus['Create User'],
                created_menus['View Users'],
                created_menus['Roles & Permissions'],
                created_menus['Activity Logs'],
            )
            self.stdout.write("✅ Created: Manager role (All menus)")
        else:
            self.stdout.write("⏭️ Already exists: Manager role")

        self.stdout.write("\n✅ Setup complete!\n")
        self.stdout.write("📋 Next steps:")
        self.stdout.write("1. Go to admin and create a test user")
        self.stdout.write("2. Assign the 'Manager' or 'Editor' role to the user")
        self.stdout.write("3. Login with the test user")
        self.stdout.write("4. You should see the sidebar menu!\n")
