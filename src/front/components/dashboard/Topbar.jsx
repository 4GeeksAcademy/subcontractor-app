import { useState } from "react";
import {
    BiSearch,
    BiBell,
    BiUser,
    BiChevronDown,
    BiCreditCard,
    BiFolder,
    BiCog,
    BiLogOut
} from "react-icons/bi";
import { useNavigate } from "react-router-dom";
import useGlobalReducer from "../../hooks/useGlobalReducer";

export const Topbar = ({ isMobile }) => {
    const [isProfileDropdownOpen, setIsProfileDropdownOpen] = useState(false);
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

    const { store, dispatch } = useGlobalReducer()
    const navigate = useNavigate()

    const mobileMenuItems = [
        { name: "Payments", icon: BiCreditCard, path: "/dashboard/payments" },
        { name: "Portfolio", icon: BiFolder, path: "/dashboard/portfolio" },
        { name: "Settings", icon: BiCog, path: "/dashboard/settings" }
    ];

    const handleLogout = () => {
        localStorage.removeItem('provider')
        localStorage.removeItem('token')
        dispatch({ type: 'logout' })
        setIsProfileDropdownOpen(false)
        navigate('/?action=login')
    };

    return (
        <header className="topbar">
            <div className="container-fluid">
                <div className="topbar-inner">
                    {/* Left: Search */}
                    <div className="topbar-left">
                        <div className="search-container">
                            <div className="search-input-wrapper">
                                <BiSearch className="search-icon" />
                                <input
                                    type="text"
                                    placeholder="Search..."
                                    className="search-input form-control"
                                />
                            </div>
                        </div>
                    </div>

                    {/* Right: Notifications & Profile */}
                    <div className="topbar-right">
                        {/* Notifications */}
                        <button className="notification-btn btn btn-link position-relative">
                            <BiBell className="notification-icon" />
                            <span className="notification-badge"></span>
                        </button>

                        {/* Desktop Profile Dropdown */}
                        {!isMobile && (
                            <div className="profile-dropdown">
                                <button
                                    onClick={() => setIsProfileDropdownOpen(!isProfileDropdownOpen)}
                                    className="profile-btn d-flex align-items-center"
                                >
                                    <div className="profile-avatar">
                                        <BiUser className="profile-avatar-icon" />
                                    </div>
                                    <span className="profile-name"> {store.provider ? store.provider.name : 'Contractor'}</span>
                                    <BiChevronDown className={`profile-dropdown-icon ${isProfileDropdownOpen ? 'rotate' : ''}`} />
                                </button>

                                {/* Dropdown Menu */}
                                {isProfileDropdownOpen && (
                                    <div className="profile-menu">
                                        <a href="#" className="profile-menu-item">
                                            <BiUser className="profile-menu-icon" />
                                            Profile
                                        </a>
                                        <a href="#" className="profile-menu-item">
                                            <BiCreditCard className="profile-menu-icon" />
                                            Payments
                                        </a>
                                        <a href="#" className="profile-menu-item">
                                            <BiFolder className="profile-menu-icon" />
                                            Portfolio
                                        </a>
                                        <a href="#" className="profile-menu-item">
                                            <BiCog className="profile-menu-icon" />
                                            Settings
                                        </a>
                                        <hr className="profile-menu-divider" />
                                        <button onClick={handleLogout} className="profile-menu-item profile-menu-logout">
                                            <BiLogOut className="profile-menu-icon" />
                                            Logout
                                        </button>
                                    </div>
                                )}
                            </div>
                        )}

                        {/* Mobile Menu Button */}
                        {isMobile && (
                            <button
                                onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                                className="mobile-menu-btn btn btn-link"
                            >
                                <BiChevronDown className={`mobile-menu-icon ${isMobileMenuOpen ? 'rotate' : ''}`} />
                            </button>
                        )}
                    </div>
                </div>

                {/* Mobile Menu */}
                {isMobile && isMobileMenuOpen && (
                    <div className="mobile-menu">
                        <div className="mobile-menu-inner">
                            {mobileMenuItems.map((item) => {
                                const Icon = item.icon;
                                return (
                                    <a
                                        key={item.name}
                                        href={item.path}
                                        className="mobile-menu-item"
                                    >
                                        <Icon className="mobile-menu-icon" />
                                        {item.name}
                                    </a>
                                );
                            })}
                            <hr className="mobile-menu-divider" />
                            <button onClick={handleLogout} className="mobile-menu-item mobile-menu-logout">
                                <BiLogOut className="mobile-menu-icon" />
                                Logout
                            </button>
                        </div>
                    </div>
                )}
            </div>
        </header>
    );
};
