

document.addEventListener('DOMContentLoaded', function () {
    const html = document.documentElement;
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');
    const toggleBtn = document.getElementById('toggleSidebar');
    const themeToggle = document.getElementById('themeToggle');
    const profileBtn = document.getElementById('profileBtn');
    const profileMenu = document.getElementById('profileMenu');
    const notifBtn = document.getElementById('notificationBtn');
    const notifMenu = document.getElementById('notificationMenu');
    const sidebarNav = document.getElementById('sidebarNav');
    const DESKTOP = 768;

    function normalizePath(path) {
        if (!path) return '/';
        try {
            const url = new URL(path, window.location.origin);
            return url.pathname.replace(/\/+$/, '') || '/';
        } catch (e) {
            return (path || '').replace(/\/+$/, '') || '/';
        }
    }

    function navigateMainContent(url, source = null) {
        if (typeof htmx !== 'undefined') {
            htmx.ajax('GET', url, {
                source: source || undefined,
                target: '#main-content',
                select: '#main-content',
                swap: 'outerHTML'
            });
        } else {
            window.location.href = url;
        }
    }

    function setTheme(theme) {
        html.classList.toggle('dark', theme === 'dark');
        localStorage.setItem('theme', theme);

        if (themeToggle) {
            const icon = themeToggle.querySelector('i');
            if (icon) {
                icon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
            }
        }
    }

    (function initTheme() {
        const savedTheme = localStorage.getItem('theme');
        const systemDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        setTheme(savedTheme || (systemDark ? 'dark' : 'light'));
    })();

    themeToggle?.addEventListener('click', function () {
        setTheme(html.classList.contains('dark') ? 'light' : 'dark');
    });

    const isDesktop = () => window.innerWidth >= DESKTOP;

    function applyDesktopState() {
        if (!sidebar || !isDesktop()) return;

        const collapsed = localStorage.getItem('desktopSidebarCollapsed') === 'true';

        sidebar.classList.remove('sidebar-hover-expand');
        sidebar.classList.toggle('sidebar-collapsed', collapsed);
        sidebar.classList.toggle('sidebar-open', !collapsed);

        if (collapsed) {
            document.querySelectorAll('.dropdown-menu').forEach(menu => {
                menu.classList.add('hidden');
            });

            document.querySelectorAll('.chevron').forEach(icon => {
                icon.classList.remove('rotate-180');
            });
        }
    }

    function openMobile() {
        if (!sidebar || !overlay) return;
        sidebar.classList.remove('-translate-x-full');
        overlay.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
    }

    function closeMobile() {
        if (!sidebar || !overlay) return;
        sidebar.classList.add('-translate-x-full');
        overlay.classList.add('hidden');
        document.body.style.overflow = '';
    }

    function syncSidebar() {
        if (!sidebar) return;

        if (isDesktop()) {
            sidebar.classList.remove('-translate-x-full');
            overlay?.classList.add('hidden');
            document.body.style.overflow = '';
            applyDesktopState();
        } else {
            sidebar.classList.remove('sidebar-collapsed');
            sidebar.classList.remove('sidebar-hover-expand');
            sidebar.classList.add('sidebar-open');
            sidebar.classList.add('-translate-x-full');
            overlay?.classList.add('hidden');
            document.body.style.overflow = '';
        }
    }

    function setActiveSidebarLinks() {
        const currentPath = normalizePath(window.location.pathname);

        document.querySelectorAll('.sidebar-link, .sidebar-child-link').forEach(link => {
            link.classList.remove('active');
        });

        document.querySelectorAll('.dropdown-trigger').forEach(trigger => {
            trigger.classList.remove('active');
        });

        document.querySelectorAll('.dropdown-menu').forEach(menu => {
            menu.classList.add('hidden');
        });

        document.querySelectorAll('.chevron').forEach(icon => {
            icon.classList.remove('rotate-180');
        });

        document.querySelectorAll('.sidebar-link, .sidebar-child-link').forEach(link => {
            const href = normalizePath(link.getAttribute('href'));

            if (href === currentPath) {
                link.classList.add('active');

                const dropdownMenu = link.closest('.dropdown-menu');
                if (dropdownMenu) {
                    dropdownMenu.classList.remove('hidden');

                    const sidebarGroup = link.closest('.sidebar-group');
                    sidebarGroup?.querySelector('.dropdown-trigger')?.classList.add('active');
                    sidebarGroup?.querySelector('.chevron')?.classList.add('rotate-180');
                }
            }
        });

        if (isDesktop() && sidebar?.classList.contains('sidebar-collapsed') && !sidebar.classList.contains('sidebar-hover-expand')) {
            document.querySelectorAll('.dropdown-menu').forEach(menu => {
                menu.classList.add('hidden');
            });
        }
    }

    sidebar?.addEventListener('mouseenter', function () {
        if (isDesktop() && sidebar.classList.contains('sidebar-collapsed')) {
            sidebar.classList.add('sidebar-hover-expand');
        }
    });

    sidebar?.addEventListener('mouseleave', function () {
        sidebar.classList.remove('sidebar-hover-expand');
        setActiveSidebarLinks();
    });

    toggleBtn?.addEventListener('click', function () {
        if (isDesktop()) {
            const currentlyCollapsed = localStorage.getItem('desktopSidebarCollapsed') === 'true';
            localStorage.setItem('desktopSidebarCollapsed', String(!currentlyCollapsed));
            applyDesktopState();
            setActiveSidebarLinks();
        } else {
            if (sidebar?.classList.contains('-translate-x-full')) {
                openMobile();
            } else {
                closeMobile();
            }
        }
    });

    overlay?.addEventListener('click', closeMobile);
    window.addEventListener('resize', function () {
        syncSidebar();
        setActiveSidebarLinks();
    });

    document.querySelectorAll('.dropdown-trigger').forEach(trigger => {
        trigger.addEventListener('click', function (e) {
            e.preventDefault();
            e.stopPropagation();

            if (
                isDesktop() &&
                sidebar?.classList.contains('sidebar-collapsed') &&
                !sidebar.classList.contains('sidebar-hover-expand')
            ) {
                return;
            }

            const group = this.closest('.sidebar-group');
            if (!group) return;

            group.querySelector('.dropdown-menu')?.classList.toggle('hidden');
            group.querySelector('.chevron')?.classList.toggle('rotate-180');
            this.classList.toggle('active');
        });
    });

    function bindPopup(button, menu, otherMenu) {
        if (!button || !menu) return;

        button.addEventListener('click', function (e) {
            e.stopPropagation();
            menu.classList.toggle('hidden');
            otherMenu?.classList.add('hidden');
        });

        menu.addEventListener('click', function (e) {
            e.stopPropagation();
        });
    }

    bindPopup(profileBtn, profileMenu, notifMenu);
    bindPopup(notifBtn, notifMenu, profileMenu);

    document.addEventListener('click', function () {
        profileMenu?.classList.add('hidden');
        notifMenu?.classList.add('hidden');
    });

    sidebarNav?.addEventListener('click', function (e) {
        const link = e.target.closest('a.sidebar-link, a.sidebar-child-link');
        if (!link) return;

        const rawHref = link.getAttribute('href');
        if (!rawHref || rawHref.startsWith('#') || rawHref.startsWith('javascript:')) return;

        const nextUrl = new URL(rawHref, window.location.origin);
        const nextFullPath = `${normalizePath(nextUrl.pathname)}${nextUrl.search}`;
        const currentUrl = new URL(window.location.href);
        const currentFullPath = `${normalizePath(currentUrl.pathname)}${currentUrl.search}`;

        const href = normalizePath(rawHref);
        const currentPath = normalizePath(window.location.pathname);

        // Sidebar navigation is fully HTMX-driven to avoid mixed handlers requiring double click.
        e.preventDefault();
        e.stopPropagation();

        // Keep browser URL in sync so active state resolver uses the correct route.
        if (nextFullPath !== currentFullPath) {
            window.history.pushState({ htmx: true }, '', `${nextUrl.pathname}${nextUrl.search}${nextUrl.hash}`);
        }

        navigateMainContent(rawHref, link);

        if (href !== currentPath) {
            document.querySelectorAll('.sidebar-link, .sidebar-child-link').forEach(item => {
                item.classList.remove('active');
            });
            link.classList.add('active');
        }

        if (!isDesktop()) {
            closeMobile();
        }
    });

    document.body.addEventListener('htmx:afterSwap', function (e) {
        const target = e?.detail?.target || e.target;
        const hasMainContent = !!(target && (target.id === 'main-content' || target.querySelector?.('#main-content')));
        if (!hasMainContent) return;

        setActiveSidebarLinks();

        if (typeof window.syncPageChromeFromMainContent === 'function') {
            window.syncPageChromeFromMainContent();
        }

        const newMain = document.getElementById('main-content');
        if (newMain) {
            newMain.scrollTop = 0;
        }

        if (!isDesktop()) {
            closeMobile();
        }
    });

    document.body.addEventListener('htmx:historyRestore', function () {
        setActiveSidebarLinks();
    });

    window.addEventListener('popstate', function () {
        navigateMainContent(window.location.href, sidebarNav || document.body);
        setActiveSidebarLinks();
        if (typeof window.syncPageChromeFromMainContent === 'function') {
            window.syncPageChromeFromMainContent();
        }
    });

    syncSidebar();
    setActiveSidebarLinks();
});