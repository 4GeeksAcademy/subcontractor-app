import { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import useGlobalReducer from "../../hooks/useGlobalReducer";
import {
    BiGridAlt,
    BiFile,
    BiBriefcase,
    BiGroup,
    BiReceipt,
    BiCreditCard,
    BiCog,
    BiFolder,
    BiMenu,
    BiX
} from "react-icons/bi";

export const Sidebar = ({ isCollapsed, toggleCollapse, isMobile, isMobileOpen, toggleMobile }) => {
    const location = useLocation();
    const { store, dispatch } = useGlobalReducer()

    const menuItems = [
        { name: "Dashboard", icon: BiGridAlt, path: "/providerdashboard" },
        { name: "Estimate Requests", icon: BiFile, path: "/dashboard/estimates" },
        { name: "Jobs", icon: BiBriefcase, path: "/dashboard/jobs" },
        { name: "Customers", icon: BiGroup, path: "/dashboard/customers" },
        { name: "Invoices", icon: BiReceipt, path: "/dashboard/invoices" },
        { name: "Payments", icon: BiCreditCard, path: "/dashboard/payments" },
        { name: "Services", icon: BiCog, path: "/dashboard/services" },
        { name: "Portfolio", icon: BiFolder, path: "/dashboard/portfolio" },
        { name: "Settings", icon: BiCog, path: "/dashboard/settings" }
    ];

    const isActive = (path) => {
        return location.pathname === path || location.pathname.startsWith(path + "/");
    };

    const getInitials = (name) => {
        if (!name) return "CT";
        const nameArray = name.split(" ")
        if (nameArray.length === 1) {
            return nameArray[0].charAt(0).toUpperCase()
        }
        return nameArray[0].charAt(0) + nameArray[nameArray.length - 1].charAt(0).toUpperCase()
    }
    console.log("debuging name", store.provider)

    return (
        <>
            {/* Mobile overlay */}
            {isMobile && isMobileOpen && (
                <div
                    className="sidebar-overlay d-lg-none"
                    onClick={toggleMobile}
                />
            )}

            {/* Sidebar */}
            <div className={`sidebar d-flex flex-column ${isCollapsed ? 'collapsed' : ''} ${isMobile ? (isMobileOpen ? 'mobile-open' : 'mobile-closed') : ''}`}>
                {/* Logo/Header */}
                <div className="sidebar-header d-flex align-items-center justify-content-between p-3 border-bottom">
                    {!isCollapsed && (
                        <div className="d-flex align-items-center">
                            <div className="sidebar-logo me-3">
                                <BiBriefcase className="sidebar-logo-icon" />
                            </div>
                            <span className="sidebar-title">Dashboard</span>
                        </div>
                    )}
                    <button
                        onClick={isMobile ? toggleMobile : toggleCollapse}
                        className="sidebar-toggle btn btn-link text-white"
                    >
                        {isMobile ? (
                            <BiX className="sidebar-toggle-icon" />
                        ) : (
                            <BiMenu className="sidebar-toggle-icon" />
                        )}
                    </button>
                </div>

                {/* Navigation */}
                <nav className="sidebar-nav flex-grow-1 p-3">
                    <ul className="list-unstyled">
                        {menuItems.map((item) => {
                            const Icon = item.icon;
                            return (
                                <li key={item.name} className="mb-2">
                                    <Link
                                        to={item.path}
                                        className={`sidebar-link d-flex align-items-center text-decoration-none ${isActive(item.path) ? 'active' : ''
                                            }`}
                                        onClick={isMobile ? toggleMobile : undefined}
                                    >
                                        <Icon className={`sidebar-link-icon ${isActive(item.path) ? 'active' : ''}`} />
                                        {!isCollapsed && (
                                            <span className="sidebar-link-text">{item.name}</span>
                                        )}
                                    </Link>
                                </li>
                            );
                        })}
                    </ul>
                </nav>

                {/* User section */}
                {!isCollapsed && (
                    <div className="sidebar-user p-3 border-top">
                        <div className="d-flex align-items-center">
                            <div className="sidebar-user-avatar me-3">
                                <span className="sidebar-user-initials">
                                    {store.provider ? getInitials(store.provider.name) : "CT"}
                                </span>
                            </div>
                            <div className="flex-grow-1">
                                <p className="sidebar-user-name mb-0"> {store.provider ? store.provider?.name : "Contractor"} </p>
                                <p className="sidebar-user-role mb-0">Provider</p>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </>
    );
};
