import { Link, useLocation } from "react-router-dom";
import {
    BiGridAlt,
    BiFile,
    BiBriefcase,
    BiGroup,
    BiReceipt,
    BiCog
} from "react-icons/bi";

export const BottomNavigation = () => {
    const location = useLocation();

    const menuItems = [
        { name: "Dashboard", icon: BiGridAlt, path: "/dashboard" },
        { name: "Estimates", icon: BiFile, path: "/dashboard/estimates" },
        { name: "Jobs", icon: BiBriefcase, path: "/dashboard/jobs" },
        { name: "Customers", icon: BiGroup, path: "/dashboard/customers" },
        { name: "Invoices", icon: BiReceipt, path: "/dashboard/invoices" },
        { name: "Services", icon: BiCog, path: "/dashboard/services" }
    ];

    const isActive = (path) => {
        return location.pathname === path || location.pathname.startsWith(path + "/");
    };

    return (
        <div className="bottom-nav fixed-bottom d-lg-none">
            <div className="bottom-nav-inner d-flex justify-content-around align-items-center h-100">
                {menuItems.map((item) => {
                    const Icon = item.icon;
                    const active = isActive(item.path);

                    return (
                        <Link
                            key={item.name}
                            to={item.path}
                            className={`bottom-nav-item d-flex flex-column align-items-center text-decoration-none ${active ? 'active' : ''
                                }`}
                        >
                            <Icon className={`bottom-nav-icon ${active ? 'text-primary' : 'text-secondary'}`} />
                            <span className={`bottom-nav-label ${active ? 'text-primary' : 'text-secondary'}`}>
                                {item.name}
                            </span>
                        </Link>
                    );
                })}
            </div>
        </div>
    );
};
