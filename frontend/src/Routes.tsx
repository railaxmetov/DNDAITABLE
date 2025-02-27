import { createBrowserRouter} from "react-router-dom";
import LandingPage from "./pages/LandingPage.tsx";
import LoginForm from "./pages/LoginForm.tsx";
import RegisterForm from "./pages/RegisterForm.tsx";
import ProfilePage from "./pages/ProfilePage.tsx";
import ChatRoom from "./pages/ChatRoom.tsx";

export const router = createBrowserRouter([
    {
        path: "/",
        element: <LandingPage/>
    },
    {
        path: "/login",
        element: <LoginForm/>
    },
    {
        path: "/regist",
        element: <RegisterForm/>
    },
    {
        path: "/profile",
        element: <ProfilePage/>
    },
    {
        path: "/chat_room",
        element: <ChatRoom/>
    }
])