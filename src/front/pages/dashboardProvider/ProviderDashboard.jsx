import { useEffect } from "react";
import { DashboardLayout } from "../../components/dashboard/DashboardLayout";
import { Outlet } from "react-router-dom";
import useGlobalReducer from "../../hooks/useGlobalReducer";

export const ProviderDashboard = () => {

    const { store, dispatch } = useGlobalReducer()

    useEffect(() => {
        const backdrops = document.querySelectorAll('.modal-backdrop');
        backdrops.forEach(b => b.remove());

        document.body.classList.remove('modal-open');
        document.body.style.overflow = 'auto';
        document.body.style.paddingRight = '0';
    }, []);

    return (
        <DashboardLayout>
            <Outlet />
        </DashboardLayout>
    );
};