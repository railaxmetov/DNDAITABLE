import {useState} from "react";

export default function ChatInput(props: any) {
    const [message, setMessage] = useState<string>("");

    const sendMessage = () => {
        props.socket.emit("data", {'message': message, 'nickname': sessionStorage.getItem("nickname")});
        setMessage("");
    }

    return (
        <div className="chat_input">
            <input type='text' placeholder='Message type here...' onChange={(e) => setMessage(e.target.value)}
                   value={message}/>
            <input type='button' onClick={sendMessage}/>
        </div>
    )

}