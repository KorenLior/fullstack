import { useState } from 'react';
import type { FormEvent } from 'react';
import Table from './table';

const TASKS_ENDPOINT = 'http://localhost:8000/api/items';

async function readTask(id: string) {
    const trimmed = id.trim();
    if (trimmed === '') {
        throw new Error('Please enter an ID.');
    }

    const response = await fetch(`${TASKS_ENDPOINT}?id=${trimmed}`);
    if (!response.ok) {
        throw new Error('Failed to fetch task.');
    }

    return response.json() as Promise<string | null>;
}

async function addTask(text: string) {
    const trimmed = text.trim();
    if (trimmed === '') {
        throw new Error('Please write something to save.');
    }

    const response = await fetch(`${TASKS_ENDPOINT}?item=${trimmed}`, {
        method: 'POST'
    });
    if (!response.ok) {
        throw new Error('Failed to create task.');
    }

    return response.json() as Promise<{ id: number; item: string }>;
}

function TaskReader() {
    const [taskId, setTaskId] = useState('');
    const [task, setTask] = useState<string | null>(null);
    const [message, setMessage] = useState('Enter an ID and press "Read".');

    const onSubmit = async (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        try {
            setMessage('Looking up task…');
            const result = await readTask(taskId);
            if (result === null) {
                setTask(null);
                setMessage('No task with that ID.');
                return;
            }
            const display = typeof result === 'string' ? result : JSON.stringify(result, null, 2);
            setTask(display);
            setMessage('Task found.');
        } catch (error) {
            setTask(null);
            setMessage(error instanceof Error ? error.message : 'Something went wrong.');
        }
    };

    return (
        <section>
            <h2>Find a task</h2>
            <form onSubmit={onSubmit}>
                <input
                    value={taskId}
                    onChange={(event) => setTaskId(event.target.value)}
                    placeholder="Task ID (for example, 1)"
                />
                <button type="submit">Read</button>
            </form>
            <p>{message}</p>
            {task !== null && <p><strong>Task:</strong> {task}</p>}
        </section>
    );
}

function TaskCreator() {
    const [text, setText] = useState('');
    const [message, setMessage] = useState('Write a task and press "Create".');

    const onSubmit = async (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        try {
            setMessage('Saving task…');
            const created = await addTask(text);
            setText('');
            setMessage(`Saved task #${created.id}.`);
        } catch (error) {
            setMessage(error instanceof Error ? error.message : 'Something went wrong.');
        }
    };

    return (
        <section>
            <h2>New task</h2>
            <form onSubmit={onSubmit}>
                <input
                    value={text}
                    onChange={(event) => setText(event.target.value)}
                    placeholder="Describe the task"
                />
                <button type="submit">Create</button>
            </form>
            <p>{message}</p>
        </section>
    );
}

export default function App() {
    return (
        <main style={{ padding: '2rem', display: 'grid', gap: '2rem', maxWidth: 480 }}>
            <TaskCreator />
            <TaskReader />
            <section>
                <h2>Live counters</h2>
                <Table />
            </section>
        </main>
    );
}
