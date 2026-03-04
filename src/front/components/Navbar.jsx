import { Link } from "react-router-dom";
import { LoginProvider } from "../pages/LoginProvider";

export const Navbar = () => {

	return (
		<nav className="navbar bg-body-tertiary">
			<div className="container-fluid">
				<a className="navbar-brand">Navbar</a>

				<button type="button" className="btn btn-primary" data-bs-toggle="modal" data-bs-target="#loginModal">
					Launch static backdrop modal
				</button>

				<div className="modal fade" id="loginModal" tabIndex="-1" aria-hidden="true">
					<div className="modal-dialog modal-dialog-scrollable">
						<div className="modal-content">
							<div className="modal-header">
								<h1 className="modal-title fs-5" id="staticBackdropLabel">Modal title</h1>
								<button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
							</div>
							<div className="modal-body">
								<LoginProvider />
							</div>
							<div className="modal-footer">
								<button type="button" className="btn btn-secondary" data-bs-dismiss="modal">Close</button>
								<button type="button" className="btn btn-primary">Understood</button>
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

		// 							<li><Link to={'/signupprovider'} >Sin up Provider </Link></li>
		// 					</ul>
		// 				</li>
		// 			</ul>
		// 		</div>
		// 	</div>
		// </nav>
	);
};