import { useState } from 'react';

// Component to READ data from backend
function ReadComponent() {
    // Store what user types in the input box
    const [id, setId] = useState('');
    // Store the response from the server
    const [data, setData] = useState('');

    // This runs when user clicks "Read" button
    const handleRead = async () => {
        // Ask the backend for data with this ID
        const response = await fetch(`http://localhost:8000/api/items?id=${id}`);
        // Convert the response to JavaScript object
        const result = await response.json();
        // Save it so we can display it
        setData(result);
    };

    return (
        <div>
            <h2>Read</h2>
            {/* Input box - when user types, save it to 'id' */}
            <input value={id} onChange={e => setId(e.target.value)} placeholder="ID" />
            {/* Button - when clicked, call handleRead function */}
            <button onClick={handleRead}>Read</button>
            {/* Show the result from the server */}
            <p><strong>Result:</strong> {data || 'No data'}</p>
        </div>
    );
}

// Component to WRITE data to backend
function WriteComponent() {
    // Store what user types in the input box
    const [item, setItem] = useState('');
    // Store the response from the server
    const [result, setResult] = useState('');

    // This runs when user clicks "Write" button
    const handleWrite = async () => {
        // Send the item to the backend
        const response = await fetch(`http://localhost:8000/api/items?item=${item}`, {
            method: 'POST'  // POST means "create new data"
        });
        // Convert response to JavaScript object
        const data = await response.json();
        // Save it so we can display it
        setResult(data.message);
    };

    return (
        <div>
            <h2>Write</h2>
            {/* Input box - when user types, save it to 'item' */}
            <input value={item} onChange={e => setItem(e.target.value)} placeholder="Item text" />
            {/* Button - when clicked, call handleWrite function */}
            <button onClick={handleWrite}>Write</button>
            {/* Show the result from the server */}
            <p><strong>Result:</strong> {result || 'No result'}</p>
        </div>
    );
}

function App() {
    return (
        <div style={{ padding: '20px' }}>
            <ReadComponent />
            <WriteComponent />
        </div>
    );
}

export default App;
