import { useEffect, useState } from 'react';

function Message() {
    const [message, setMessage] = useState('Hello World');

    useEffect(() => {
        // Simple GET request to backend
        fetch('http://localhost:8000/')
            .then(res => res.json())
            .then(data => setMessage(data.message))
            .catch(err => console.error('Error:', err));
    }, []);

    return <h1>{message}</h1>;
}

export default Message;