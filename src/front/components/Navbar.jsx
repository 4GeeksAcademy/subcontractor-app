import { Link, useLocation } from "react-router-dom";
import { LoginProvider } from "../pages/LoginProvider";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faAddressBook, faUser } from "@fortawesome/free-regular-svg-icons";
import { useEffect } from "react";


export const Navbar = () => {

	const location = useLocation();
	useEffect(() => {
		const params = new URLSearchParams(location.search);

		if (params.get("openLogin") === "true") {
			const modalElement = document.getElementById('loginModal');
			if (modalElement) {
				const busModal = new window.bootstrap.Modal(modalElement);
				busModal.show();
			}
		}
	}, [location]);

	return (
		<nav className="navbar bg-body-tertiary">
			<div className="container-fluid">
				<a className="navbar-brand">Navbar</a>

				<button type="button" className="btn btn-primary" data-bs-toggle="modal" data-bs-target="#loginModal">
					<span>  <FontAwesomeIcon icon={faUser} size="" color="" /> </span> SIGN IN
				</button>

				<div className="modal fade" id="loginModal" tabIndex="-1" aria-hidden="true">
					<div className="modal-dialog modal-dialog-scrollable">
						<div className="modal-content pb-4">
							<div className="modal-header">
								<h1 className="modal-title fs-5" id="staticBackdropLabel">SIGN IN</h1>
								<button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
							</div>
							<div className="modal-body">
								<LoginProvider />
							</div>
							<div>
								<h5 className="p-3"> If you don't have an account:</h5>
							</div>
							<div className="text-center p-2">
								<Link className="border border-primary rounded-1 p-3 " style={{ textDecoration: 'none' }} to={'/signupprovider'} >
									<strong className="" data-bs-dismiss="modal"> SIGN UP HERE </strong>  </Link>
							</div>
						</div>
					</div>
				</div>
			</div>
		</nav >






		// <nav classNameName="navbar navbar-expand-lg bg-body-tertiary">
		// 	<div classNameName="container-fluid">
		// 		<a classNameName="navbar-brand" href="#">Navbar</a>
		// 		<button classNameName="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
		// 			<span classNameName="navbar-toggler-icon"></span>
		// 		</button>
		// 		<div classNameName="collapse navbar-collapse" id="navbarNavDropdown">
		// 			<ul classNameName="navbar-nav">

		// 				<li classNameName="nav-item dropdown">
		// 					<a classNameName="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
		// 						Sign up
		// 					</a>
		// 					<ul classNameName="dropdown-menu">
		// 							<li><Link to={'/signupclient'} >Sin up </Link></li>

		// 							
		// 					</ul>
		// 				</li>
		// 			</ul>
		// 		</div>
		// 	</div>
		// </nav>
	);
};