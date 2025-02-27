import {useEffect, useState} from 'react'
import {Outlet} from "react-router-dom";
import useWebSocket from "../useWebSocket.tsx";
import ChatBox from "./ChatBox.tsx";
import ChatInput from "./ChatInput.tsx";

function ChatRoom() {
    const [nickname, setNickname] = useState<string>("");
    const [messages, setMessages] = useState([])
    const socket = useWebSocket(
        'http://127.0.0.1:5000', (data: any) => {
            // @ts-ignore
            setMessages(prevMessages => [...prevMessages, data])}
    )

    useEffect(() => {
        fetchUserData();
        fetchChatData();
    }, []);

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
            setNickname(data.nickname);
        }
    };

    const fetchChatData = async () => {

        const url = `http://127.0.0.1:5000/load_chat/${sessionStorage.getItem("chat_id")}`;
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
            sessionStorage.setItem("chat_json_data", data)
        }
    };

  return (
      <>
          <h1>Chat room by {nickname}, chat id: {sessionStorage.getItem('chat_id')} </h1>
          <h2>
              Messages:
          </h2>
          <ChatBox messages={messages} socket={socket}/>
          <ChatInput socket={socket}/>
          <Outlet/>
      </>
  )
}

export default ChatRoom