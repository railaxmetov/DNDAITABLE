import React, {useState, useEffect} from "react";
import {Outlet, useNavigate} from "react-router-dom";


function LoginForm() {

    const [email, setEmail] = useState<string>("");
    const [password, setPassword] = useState<string>("");

    useEffect(() => {
        fastLogin();
    }, []);

    const navigate = useNavigate();

    const fastLogin = async () => {
        const url = "http://127.0.0.1:5000/fastlogin";
        const options = {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                'Authorization': `Bearer ${sessionStorage.getItem("access_token")}`
            }
        }
        await fetch(url, options)
            .then(response => {
                if (response.status === 200) {
                    return response.json()
                }
            })
            .then(data => {
                sessionStorage.setItem("access_token", data.access_token)
                navigate('/profile')
            })
    };

    const onSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault()
        const data = {
            email,
            password
        }
        const url = "http://127.0.0.1:5000/login";
        const options = {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),

        }
        await fetch(url, options)
            .then(response => {
                if (response.status === 200) {
                    return response.json()
                }
                else {
                    alert('error')
                }
            })
            .then(data => {
                sessionStorage.setItem("access_token", data.access_token)
                sessionStorage.setItem("refresh_token", data.refresh_token)
                navigate('/profile')
            })
            .catch(error => {
                alert(error);
            })
    };

    return <div>
        <h1>Login page</h1>
    <form className="loginForm" onSubmit={onSubmit}>
            <div className="input-label">
                <label htmlFor="email">Email:</label>
                <input type="email"
                       id="email"
                       value={email}
                       onChange={(e) => setEmail(e.target.value)}>
                </input>
            </div>

            <div className="input-label">
                <label htmlFor="password">Password:</label>
                <input type="password"
                       id="password"
                       value={password}
                       onChange={(e) => setPassword(e.target.value)}>
                </input>
            </div>
        <button type="submit">Login</button>
    </form>

            <Outlet/>
        </div>
}

export default LoginForm;