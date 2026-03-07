import { useEffect } from "react";

export const ProviderDashboard = () => {

    useEffect(() => {
        const backdrops = document.querySelectorAll('.modal-backdrop');
        backdrops.forEach(b => b.remove());

        document.body.classList.remove('modal-open');
        document.body.style.overflow = 'auto';
        document.body.style.paddingRight = '0';
    }, []);

    return (
        <div> dashboard Provider</div>
    )
}