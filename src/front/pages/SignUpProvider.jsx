import Swal from "sweetalert2";

export const SignUpProvider = () => {

    return (
        <>
            <div className="text-center bg-body-secondary p-3 ">
                <h4 className="fs-3"> SIGN UP</h4>
            </div>

            <div>
                <form class="row g-3">
                    <div class="col-12">
                        <label for="inputAddress2" class="form-label">Full Name</label>
                        <input type="text" class="form-control" id="inputAddress2" placeholder="Enter Full name" />
                    </div>
                    <div class="col-md-12">
                        <label for="inputEmail4" class="form-label">Email</label>
                        <input type="email" class="form-control" id="inputEmail4" placeholder="Enter Email" />
                    </div>
                    <div class="col-md-12">
                        <label for="inputPassword4" class="form-label">Password</label>
                        <input type="password" class="form-control" id="inputPassword4" placeholder="Enter Password" />
                    </div>
                    <div class="col-12">
                        <button type="submit" class="btn btn-primary">Sign in</button>
                    </div>
                </form>
            </div>
        </>
    )
}