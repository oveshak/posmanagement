
        // console.log('Navbar script loaded');
        // const htmlElement = document.documentElement;
        // const themeToggle = document.getElementById('themeToggle');
        // const themeToggleSettings = document.getElementById('themeToggleSettings');
        // const themeToggleSettingsKnob = document.getElementById('themeToggleSettingsKnob');

        // const sidebar = document.getElementById('sidebar');
        // const sidebarOverlay = document.getElementById('sidebarOverlay');
        // const toggleSidebar = document.getElementById('toggleSidebar');

        // const profileBtn = document.getElementById('profileBtn');
        // const profileMenu = document.getElementById('profileMenu');

        // const notificationBtn = document.getElementById('notificationBtn');
        // const notificationMenu = document.getElementById('notificationMenu');

        // const productsDropdownBtn = document.getElementById('productsDropdownBtn');
        // const productsDropdownMenu = document.getElementById('productsDropdownMenu');
        // const productsDropdownIcon = document.getElementById('productsDropdownIcon');

        // const pages = {
        //     dashboard: 'dashboard-page',
        //     sales: 'sales-page',
        //     inventory: 'inventory-page',
        //     customers: 'customers-page',
        //     orders: 'orders-page',
        //     settings: 'settings-page'
        // };

        // const pageNameMap = {
        //     dashboard: 'Dashboard',
        //     sales: 'Sales',
        //     inventory: 'Inventory',
        //     customers: 'Customers',
        //     orders: 'Orders',
        //     settings: 'Settings'
        // };

        // let salesChart = null;
        // let desktopCollapsed = false;
        // let mobileOpen = false;

        // function updateDesktopSidebarState() {
        //     if (window.innerWidth >= 768) {
        //         sidebar.classList.remove('-translate-x-full', 'translate-x-0');
        //         sidebarOverlay.classList.add('hidden');

        //         if (desktopCollapsed) {
        //             sidebar.classList.remove('sidebar-open');
        //             sidebar.classList.add('sidebar-collapsed');
        //         } else {
        //             sidebar.classList.remove('sidebar-collapsed');
        //             sidebar.classList.add('sidebar-open');
        //         }
        //     }
        // }

        // function openMobileSidebar() {
        //     mobileOpen = true;
        //     sidebar.classList.remove('-translate-x-full');
        //     sidebar.classList.add('translate-x-0');
        //     sidebarOverlay.classList.remove('hidden');
        // }

        // function closeMobileSidebar() {
        //     mobileOpen = false;
        //     sidebar.classList.add('-translate-x-full');
        //     sidebar.classList.remove('translate-x-0');
        //     sidebarOverlay.classList.add('hidden');
        // }

        // function syncSidebarOnResize() {
        //     if (window.innerWidth < 768) {
        //         sidebar.classList.remove('sidebar-collapsed');
        //         sidebar.classList.add('sidebar-open');

        //         if (mobileOpen) {
        //             openMobileSidebar();
        //         } else {
        //             closeMobileSidebar();
        //         }
        //     } else {
        //         updateDesktopSidebarState();
        //     }
        // }

        // function updateSettingsToggleUI() {
        //     const isDark = htmlElement.classList.contains('dark');

        //     if (isDark) {
        //         themeToggleSettings.classList.remove('bg-gray-300');
        //         themeToggleSettings.classList.add('bg-blue-600');
        //         themeToggleSettingsKnob.classList.add('translate-x-6');
        //     } else {
        //         themeToggleSettings.classList.remove('bg-blue-600');
        //         themeToggleSettings.classList.add('bg-gray-300');
        //         themeToggleSettingsKnob.classList.remove('translate-x-6');
        //     }
        // }

        // function applyTheme(theme) {
        //     if (theme === 'dark') {
        //         htmlElement.classList.add('dark');
        //     } else {
        //         htmlElement.classList.remove('dark');
        //     }

        //     localStorage.setItem('theme', theme);
        //     updateSettingsToggleUI();
        //     renderSalesChart();
        // }

        // function toggleTheme() {
        //     const isDark = htmlElement.classList.contains('dark');
        //     applyTheme(isDark ? 'light' : 'dark');
        // }

        // function showPage(pageId) {
        //     Object.values(pages).forEach(id => {
        //         const el = document.getElementById(id);
        //         if (el) el.classList.add('hidden');
        //     });

        //     const selectedPage = document.getElementById(pageId);
        //     if (selectedPage) selectedPage.classList.remove('hidden');

        //     const pageName = Object.keys(pages).find(key => pages[key] === pageId);
        //     const pageTitle = document.getElementById('pageTitle');

        //     if (pageTitle && pageNameMap[pageName]) {
        //         pageTitle.textContent = pageNameMap[pageName];
        //     }
        // }

        // function clearActiveLinks() {
        //     document.querySelectorAll('[data-page]').forEach(item => {
        //         item.classList.remove(
        //             'active',
        //             'bg-white/10'
        //         );
        //     });
        // }

        // function setActiveLink(link) {
        //     link.classList.add('active', 'bg-white/10');
        // }

        // function renderSalesChart() {
        //     const ctx = document.getElementById('salesChart')?.getContext('2d');
        //     if (!ctx) return;

        //     if (salesChart) salesChart.destroy();

        //     const isDarkMode = htmlElement.classList.contains('dark');
        //     const textColor = isDarkMode ? '#d1d5db' : '#374151';
        //     const gridColor = isDarkMode ? '#4b5563' : '#e5e7eb';

        //     salesChart = new Chart(ctx, {
        //         type: 'line',
        //         data: {
        //             labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        //             datasets: [{
        //                 label: 'Sales ($)',
        //                 data: [3200, 3900, 3100, 4100, 3800, 4500, 5200],
        //                 borderColor: '#3b82f6',
        //                 backgroundColor: 'rgba(59, 130, 246, 0.1)',
        //                 borderWidth: 3,
        //                 fill: true,
        //                 tension: 0.4,
        //                 pointBackgroundColor: '#3b82f6',
        //                 pointBorderColor: '#ffffff',
        //                 pointBorderWidth: 2,
        //                 pointRadius: 5,
        //                 pointHoverRadius: 7
        //             }]
        //         },
        //         options: {
        //             responsive: true,
        //             maintainAspectRatio: true,
        //             plugins: {
        //                 legend: {
        //                     labels: {
        //                         color: textColor
        //                     }
        //                 }
        //             },
        //             scales: {
        //                 y: {
        //                     ticks: { color: textColor },
        //                     grid: { color: gridColor }
        //                 },
        //                 x: {
        //                     ticks: { color: textColor },
        //                     grid: { color: gridColor }
        //                 }
        //             }
        //         }
        //     });
        // }

        // function toggleProductsDropdown() {
        //     if (window.innerWidth >= 768 && desktopCollapsed) {
        //         desktopCollapsed = false;
        //         updateDesktopSidebarState();
        //     }

        //     productsDropdownMenu.classList.toggle('hidden');
        //     productsDropdownIcon.classList.toggle('rotate-180');
        // }

        // const savedTheme = localStorage.getItem('theme') || 'light';
        // applyTheme(savedTheme);

        // themeToggle.addEventListener('click', toggleTheme);
        // themeToggleSettings.addEventListener('click', toggleTheme);

        // toggleSidebar.addEventListener('click', () => {
        //     if (window.innerWidth < 768) {
        //         if (mobileOpen) {
        //             closeMobileSidebar();
        //         } else {
        //             openMobileSidebar();
        //         }
        //     } else {
        //         desktopCollapsed = !desktopCollapsed;
        //         updateDesktopSidebarState();
        //     }
        // });

        // sidebarOverlay.addEventListener('click', closeMobileSidebar);

        // productsDropdownBtn.addEventListener('click', toggleProductsDropdown);

        // document.querySelectorAll('[data-page]').forEach(link => {
        //     link.addEventListener('click', e => {
        //         e.preventDefault();

        //         clearActiveLinks();
        //         setActiveLink(link);

        //         const pageId = pages[link.dataset.page];
        //         showPage(pageId);

        //         if (window.innerWidth < 768) {
        //             closeMobileSidebar();
        //         }
        //     });
        // });

        // profileBtn.addEventListener('click', e => {
        //     e.stopPropagation();
        //     profileMenu.classList.toggle('hidden');
        //     notificationMenu.classList.add('hidden');
        // });

        // notificationBtn.addEventListener('click', e => {
        //     e.stopPropagation();
        //     notificationMenu.classList.toggle('hidden');
        //     profileMenu.classList.add('hidden');
        // });

        // document.addEventListener('click', e => {
        //     if (!e.target.closest('#profileBtn') && !e.target.closest('#profileMenu')) {
        //         profileMenu.classList.add('hidden');
        //     }

        //     if (!e.target.closest('#notificationBtn') && !e.target.closest('#notificationMenu')) {
        //         notificationMenu.classList.add('hidden');
        //     }
        // });

        // window.addEventListener('resize', syncSidebarOnResize);

        // syncSidebarOnResize();
        // showPage('dashboard-page');
   


console.log('Navbar script loaded');

document.addEventListener('DOMContentLoaded', function () {
    const htmlElement = document.documentElement;

    const themeToggle = document.getElementById('themeToggle');
    const themeToggleSettings = document.getElementById('themeToggleSettings');
    const themeToggleSettingsKnob = document.getElementById('themeToggleSettingsKnob');

    const sidebar = document.getElementById('sidebar');
    const sidebarOverlay = document.getElementById('sidebarOverlay');
    const toggleSidebar = document.getElementById('toggleSidebar');

    const profileBtn = document.getElementById('profileBtn');
    const profileMenu = document.getElementById('profileMenu');

    const notificationBtn = document.getElementById('notificationBtn');
    const notificationMenu = document.getElementById('notificationMenu');

    const mainContent = document.getElementById('mainContent');

    const pages = {
        dashboard: 'dashboard-page',
        sales: 'sales-page',
        inventory: 'inventory-page',
        customers: 'customers-page',
        orders: 'orders-page',
        settings: 'settings-page'
    };

    const pageNameMap = {
        dashboard: 'Dashboard',
        sales: 'Sales',
        inventory: 'Inventory',
        customers: 'Customers',
        orders: 'Orders',
        settings: 'Settings'
    };

    const sidebarDropdowns = document.querySelectorAll('.sidebar-dropdown');

    let salesChart = null;
    let desktopCollapsed = false;
    let mobileOpen = false;

    function updateDesktopSidebarState() {
        if (!sidebar || !sidebarOverlay) return;

        if (window.innerWidth >= 768) {
            sidebar.classList.remove('-translate-x-full', 'translate-x-0');
            sidebarOverlay.classList.add('hidden');

            if (desktopCollapsed) {
                sidebar.classList.remove('sidebar-open');
                sidebar.classList.add('sidebar-collapsed');
            } else {
                sidebar.classList.remove('sidebar-collapsed');
                sidebar.classList.add('sidebar-open');
            }
        }
    }

    function openMobileSidebar() {
        if (!sidebar || !sidebarOverlay) return;

        mobileOpen = true;
        sidebar.classList.remove('-translate-x-full');
        sidebar.classList.add('translate-x-0');
        sidebarOverlay.classList.remove('hidden');
    }

    function closeMobileSidebar() {
        if (!sidebar || !sidebarOverlay) return;

        mobileOpen = false;
        sidebar.classList.add('-translate-x-full');
        sidebar.classList.remove('translate-x-0');
        sidebarOverlay.classList.add('hidden');
    }

    function syncSidebarOnResize() {
        if (!sidebar) return;

        if (window.innerWidth < 768) {
            sidebar.classList.remove('sidebar-collapsed');
            sidebar.classList.add('sidebar-open');

            if (mobileOpen) {
                openMobileSidebar();
            } else {
                closeMobileSidebar();
            }
        } else {
            updateDesktopSidebarState();
        }
    }

    function updateSettingsToggleUI() {
        const isDark = htmlElement.classList.contains('dark');

        if (themeToggleSettings) {
            if (isDark) {
                themeToggleSettings.classList.remove('bg-gray-300');
                themeToggleSettings.classList.add('bg-blue-600');
            } else {
                themeToggleSettings.classList.remove('bg-blue-600');
                themeToggleSettings.classList.add('bg-gray-300');
            }
        }

        if (themeToggleSettingsKnob) {
            if (isDark) {
                themeToggleSettingsKnob.classList.add('translate-x-6');
            } else {
                themeToggleSettingsKnob.classList.remove('translate-x-6');
            }
        }
    }

    function applyTheme(theme) {
        if (theme === 'dark') {
            htmlElement.classList.add('dark');
        } else {
            htmlElement.classList.remove('dark');
        }

        localStorage.setItem('theme', theme);
        updateSettingsToggleUI();
        renderSalesChart();
    }

    function toggleTheme() {
        const isDark = htmlElement.classList.contains('dark');
        applyTheme(isDark ? 'light' : 'dark');
    }

    function showPage(pageId) {
        Object.values(pages).forEach(id => {
            const el = document.getElementById(id);
            if (el) el.classList.add('hidden');
        });

        const selectedPage = document.getElementById(pageId);
        if (selectedPage) selectedPage.classList.remove('hidden');

        const pageName = Object.keys(pages).find(key => pages[key] === pageId);
        const pageTitle = document.getElementById('pageTitle');

        if (pageTitle && pageNameMap[pageName]) {
            pageTitle.textContent = pageNameMap[pageName];
        }
    }

    function clearActiveLinks() {
        document.querySelectorAll('[data-page]').forEach(item => {
            item.classList.remove('active', 'bg-white/10');
        });
    }

    function setActiveLink(link) {
        if (!link) return;
        link.classList.add('active', 'bg-white/10');
    }

    function renderSalesChart() {
        const canvas = document.getElementById('salesChart');
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        if (salesChart) salesChart.destroy();

        const isDarkMode = htmlElement.classList.contains('dark');
        const textColor = isDarkMode ? '#d1d5db' : '#374151';
        const gridColor = isDarkMode ? '#4b5563' : '#e5e7eb';

        salesChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                datasets: [{
                    label: 'Sales ($)',
                    data: [3200, 3900, 3100, 4100, 3800, 4500, 5200],
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#3b82f6',
                    pointBorderColor: '#ffffff',
                    pointBorderWidth: 2,
                    pointRadius: 5,
                    pointHoverRadius: 7
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        labels: {
                            color: textColor
                        }
                    }
                },
                scales: {
                    y: {
                        ticks: { color: textColor },
                        grid: { color: gridColor }
                    },
                    x: {
                        ticks: { color: textColor },
                        grid: { color: gridColor }
                    }
                }
            }
        });
    }

    function setupSidebarDropdowns() {
        sidebarDropdowns.forEach(dropdown => {
            const trigger = dropdown.querySelector('.dropdown-trigger');
            const menu = dropdown.querySelector('.dropdown-menu-wrap');
            const icon = dropdown.querySelector('.dropdown-icon');

            if (!trigger || !menu || !icon) return;

            trigger.addEventListener('click', () => {
                const isHidden = menu.classList.contains('hidden');

                sidebarDropdowns.forEach(item => {
                    const otherMenu = item.querySelector('.dropdown-menu-wrap');
                    const otherIcon = item.querySelector('.dropdown-icon');

                    if (item !== dropdown && otherMenu && otherIcon) {
                        otherMenu.classList.add('hidden');
                        otherIcon.classList.remove('rotate-180');
                    }
                });

                if (window.innerWidth >= 768 && desktopCollapsed) {
                    desktopCollapsed = false;
                    updateDesktopSidebarState();
                }

                if (isHidden) {
                    menu.classList.remove('hidden');
                    icon.classList.add('rotate-180');
                } else {
                    menu.classList.add('hidden');
                    icon.classList.remove('rotate-180');
                }
            });
        });
    }

    const savedTheme = localStorage.getItem('theme') || 'light';
    applyTheme(savedTheme);

    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
    }

    if (themeToggleSettings) {
        themeToggleSettings.addEventListener('click', toggleTheme);
    }

    if (toggleSidebar) {
        toggleSidebar.addEventListener('click', () => {
            if (window.innerWidth < 768) {
                if (mobileOpen) {
                    closeMobileSidebar();
                } else {
                    openMobileSidebar();
                }
            } else {
                desktopCollapsed = !desktopCollapsed;
                updateDesktopSidebarState();
            }
        });
    }

    if (sidebarOverlay) {
        sidebarOverlay.addEventListener('click', closeMobileSidebar);
    }

    document.querySelectorAll('[data-page]').forEach(link => {
        link.addEventListener('click', e => {
            e.preventDefault();

            clearActiveLinks();
            setActiveLink(link);

            const pageId = pages[link.dataset.page];
            if (pageId) showPage(pageId);

            if (window.innerWidth < 768) {
                closeMobileSidebar();
            }
        });
    });

    if (profileBtn && profileMenu) {
        profileBtn.addEventListener('click', e => {
            e.stopPropagation();
            profileMenu.classList.toggle('hidden');
            if (notificationMenu) notificationMenu.classList.add('hidden');
        });
    }

    if (notificationBtn && notificationMenu) {
        notificationBtn.addEventListener('click', e => {
            e.stopPropagation();
            notificationMenu.classList.toggle('hidden');
            if (profileMenu) profileMenu.classList.add('hidden');
        });
    }

    document.addEventListener('click', e => {
        if (profileMenu && !e.target.closest('#profileBtn') && !e.target.closest('#profileMenu')) {
            profileMenu.classList.add('hidden');
        }

        if (notificationMenu && !e.target.closest('#notificationBtn') && !e.target.closest('#notificationMenu')) {
            notificationMenu.classList.add('hidden');
        }
    });

    window.addEventListener('resize', syncSidebarOnResize);

    setupSidebarDropdowns();
    syncSidebarOnResize();
    showPage('dashboard-page');
});