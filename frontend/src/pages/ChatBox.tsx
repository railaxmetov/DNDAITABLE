import ChatMessage from "./ChatMessage.tsx";

export default function ChatBox(props: { messages: any[]; socket: any; }) {
    return (
        <div>
            {props.messages.map((message, i) => (
                <ChatMessage key={i} message={message} />
            ))}
        </div>
    )
}