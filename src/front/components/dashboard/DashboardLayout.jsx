import { useState, useEffect } from "react";
import { Sidebar } from "./Sidebar";
import { Topbar } from "./Topbar";
import { BottomNavigation } from "./BottomNavigation";
import "../../styles/dashboard.css";

export const DashboardLayout = ({ children }) => {
    const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
    const [isMobile, setIsMobile] = useState(false);
    const [isMobileSidebarOpen, setIsMobileSidebarOpen] = useState(false);

    useEffect(() => {
        const checkMobile = () => {
            const mobile = window.innerWidth < 992;
            setIsMobile(mobile);
            if (mobile) {
                setIsSidebarCollapsed(false);
                setIsMobileSidebarOpen(false);
            }
        };

        checkMobile();
        window.addEventListener('resize', checkMobile);
        return () => window.removeEventListener('resize', checkMobile);
    }, []);

    const toggleSidebarCollapse = () => {
        setIsSidebarCollapsed(!isSidebarCollapsed);
    };

    const toggleMobileSidebar = () => {
        setIsMobileSidebarOpen(!isMobileSidebarOpen);
    };

    return (
        <div className="dashboard-layout">
            {/* Sidebar */}
            <Sidebar
                isCollapsed={isSidebarCollapsed}
                toggleCollapse={toggleSidebarCollapse}
                isMobile={isMobile}
                isMobileOpen={isMobileSidebarOpen}
                toggleMobile={toggleMobileSidebar}
            />

            {/* Main Content */}
            <div className={`dashboard-main ${isSidebarCollapsed ? 'sidebar-collapsed' : ''}`}>
                {/* Topbar */}
                <Topbar isMobile={isMobile} />

                {/* Page Content */}
                <main className="dashboard-content">
                    <div className="dashboard-content-inner">
                        {children}
                    </div>
                </main>

                {/* Bottom Navigation for Mobile */}
                <BottomNavigation />
            </div>
        </div>
    );
};
