import {Link, Outlet} from "react-router-dom";

function LandingPage() {
    return (
        <>
            <h1>LandingPage</h1>
            <Link to="/login">
                <button type="button">Login</button>
            </Link>
            <Link to="/regist">
                <button type="button">Register</button>
            </Link>
            <Outlet/>
        </>
    );
}

export default LandingPage