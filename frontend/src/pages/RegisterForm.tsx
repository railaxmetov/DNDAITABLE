import React, {useState} from "react";
import {Outlet} from "react-router-dom";

function RegisterForm() {

    const [nickname, setNickname] = useState<string>("");
    const [email, setEmail] = useState<string>("");
    const [password, setPassword] = useState<string>("");
    const [repeatPassword, setRepeatPassword] = useState<string>("");

    const onSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const data = {
            nickname,
            email,
            password,
            repeatPassword
        }
        const url = "http://127.0.0.1:5000/regist";
        console.log(url)
        const options = {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        }
        const response = await fetch(url, options)
        if (response.status !== 200 && response.status !== 201) {
            const error_data = await response.json()
            alert(error_data.message)
        } else {
            // Successful
        }
    }

    return <div>
        <h1>Register page</h1>
        <form className="registerForm" onSubmit={onSubmit}>
            <div className="input-label">
                <label htmlFor="nickname">Nickname:</label>
                <input type="text"
                       id="nickname"
                       value={nickname}
                       onChange={(e) => setNickname(e.target.value)}>
                </input>
            </div>

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

            <div className="input-label">
                <label htmlFor="repeatPassword">Repeat password:</label>
                <input type="password"
                       id="repeatPassword"
                       value={repeatPassword}
                       onChange={(e) => setRepeatPassword(e.target.value)}>
                </input>
            </div>
                <button type="submit">Register</button>
        </form>
        <Outlet/>
    </div>
}

export default RegisterForm;