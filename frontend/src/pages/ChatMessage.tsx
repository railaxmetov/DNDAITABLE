export default function ChatMessage(props: { message: any;}) {
    const {message} = props;

    return (
        <div className='chat_message'>
            <p>{message.nickname}: {message.message}</p>
        </div>
    )
}