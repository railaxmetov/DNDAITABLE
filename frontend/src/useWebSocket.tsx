import {useState, useEffect} from "react";
import {io} from "socket.io-client";


export default function useWebSocket(url: string, dataHandler: any) {
    const [socket, setSocket] = useState<any>(null)

    useEffect(() => {
        const socketClient = io(url)

        socketClient.on('connect', () => {
            console.log('Connected to server')
        });

        socketClient.on('disconnect', () => {
            console.log('Disconnected from server')
        });

        socketClient.on('data', (data: any) => {
            dataHandler(data)
        });

        setSocket(socketClient);

        return () => {
            socketClient.close();
        }
    }, []);

    return socket;
}