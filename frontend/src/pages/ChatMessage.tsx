export default function ChatMessage(props: { message: any; socketID: any; }) {
    const {message, socketID} = props;
    const ownMessage = message.socketID === socketID;

    return (
        <div className='chat_message'>
            <p>{ownMessage ? 'You' : message.data.nickname}: {message.data.message}</p>
        </div>
    )
}