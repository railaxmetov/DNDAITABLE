import {useEffect, useState} from 'react'
import {Outlet, useNavigate} from "react-router-dom";

function ProfilePage() {
    const [nickname, setNickname] = useState("");
    let [chats, setChats] = useState<chatInterface[]>([]);
    useEffect(() => {
        fetchUserData();
        loadChats(setChats);
    }, []);

    const navigate = useNavigate();

    const fetchUserData = async () => {

        const url = "http://127.0.0.1:5000/profile";
        const options = {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                'Authorization': `Bearer ${sessionStorage.getItem("access_token")}`
            }
        }
        const response = await fetch(url, options)
        if (response.status !== 200 && response.status !== 201) {
            const error_data = await response.json()
            alert(error_data.message)
        }
        else {
            const data = await response.json()
            sessionStorage.setItem('nickname', data.nickname)
            setNickname(data.nickname);
        }
    };

    const revoke = async () => {

        let url = "http://127.0.0.1:5000/revoke_access";
        let options = {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
                'Authorization': `Bearer ${sessionStorage.getItem("access_token")}`
            }
        }
        let response = await fetch(url, options)
        if (response.status !== 200 && response.status !== 201) {
            const error_data = await response.json()
            alert(error_data.message)
        }
        else {
            sessionStorage.setItem("access_token", '')
        }

        url = "http://127.0.0.1:5000/revoke_refresh";
        options = {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
                'Authorization': `Bearer ${sessionStorage.getItem("refresh_token")}`
            }
        }
        response = await fetch(url, options)
        if (response.status !== 200 && response.status !== 201) {
            const error_data = await response.json()
            alert(error_data.message)
        }
        else {
            sessionStorage.setItem("refresh_token", '')
        }
        navigate('/login')
    };

    interface chatInterface {
        id: string;
        name: string;
    }

    const loadChats = async (setChats: any) => {
        let url = "http://127.0.0.1:5000/chats";
        let options = {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                'Authorization': `Bearer ${sessionStorage.getItem("access_token")}`
            }
        }
        let response = await fetch(url, options)
        if (response.status !== 200 && response.status !== 201) {
            const error_data = await response.json()
            alert(error_data.message)
        }
        else {
            const data = await response.json()
            setChats(data.chats)
        }
    }

    const createChat = async () => {
        let url = "http://127.0.0.1:5000/create_chat";
        let options = {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                'Authorization': `Bearer ${sessionStorage.getItem("access_token")}`
            }
        }
        let response = await fetch(url, options)
        if (response.status !== 200 && response.status !== 201) {
            const error_data = await response.json()
            alert(error_data.message)
        }
        else {
            const data = await response.json()
            sessionStorage.setItem("chat_id", data.chat_id);
        }

        navigate('/chat_room')
    }

    const loadChat = async (chat_id: string) => {
        sessionStorage.setItem("chat_id", chat_id);
        navigate('/chat_room')
    }

    const listOfChats = chats.map(ch =>
        <li>
            <p>{ch.id}{ch.name}</p>
            <button className="modal-open"
                    onClick={() => loadChat(ch.id)}>
                Select
            </button>
        </li>
    )

    return (
        <>
            <div className="nickname-header">
              <h1>{nickname}</h1>
          </div>
          <div>
              <button className="modal-close" onClick={revoke}>
                  Log out
              </button>
          </div>
          <div>
              <button className="modal-open" onClick={createChat}>
                  Start new chat
              </button>
          </div>
          <div>
              <ul>
                  {listOfChats}
              </ul>
          </div>
          <Outlet/>
      </>
  )
}

export default ProfilePage