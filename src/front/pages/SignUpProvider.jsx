import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Swal from "sweetalert2";

export const SignUpProvider = () => {

    const navigate = useNavigate()
    const [form, setform] = useState({ name: '', email: '', password: '', })

    const handleChange = (e) => {
        setform({ ...form, [e.target.name]: e.target.value })
    }

    const handleRegister = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}api/user/provider/register`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(form)
            });
            const data = await response.json()

            if (response.ok) {
                Swal.fire({
                    title: "Registered successfully!",
                    text: "Your account has been created. Please log in to access your dashboard.",
                    icon: "success",
                    confirmButtonText: "Go to Login",
                    confirmButtonColor: "#035aa6"
                }).then((result) => {
                    if (result.isConfirmed) {
                        navigate("/loginprovider");
                    }
                });
            } else {
                Swal.fire({
                    title: "Error",
                    text: data.msg || "There was an issue with your registration.",
                    icon: "error",
                    confirmButtonColor: "#d33"
                });
            }


        } catch (error) {
            console.error("Error connexion when sign up.", error)
        }
    }


    return (
        <>
            <div className="text-center bg-body-secondary p-3 ">
                <h4 className="fs-3"> SIGN UP</h4>
            </div>

            <div>
                <form class="row g-3" onSubmit={handleRegister}>
                    <div class="col-12">
                        <label for="inputAddress2" class="form-label">Full Name</label>
                        <input type="text" class="form-control" id="inputAddress2" placeholder="Enter Full name"
                            onChange={handleChange} name="name" />
                    </div>
                    <div class="col-md-12">
                        <label for="inputEmail4" class="form-label">Email</label>
                        <input type="email" class="form-control" id="inputEmail4" placeholder="Enter Email"
                            onChange={handleChange} name="email" />
                    </div>
                    <div class="col-md-12">
                        <label for="inputPassword4" class="form-label">Password</label>
                        <input type="password" class="form-control" id="inputPassword4" placeholder="Enter Password"
                            onChange={handleChange} name="password" />
                    </div>
                    <div class="col-12">
                        <button type="submit" class="btn btn-primary">Sign Up</button>
                    </div>
                </form>
            </div>
        </>
    )
}