import { useEffect, useSyncExternalStore } from "react";

type Table = Record<number, number>;

let state: Table = {};
const listeners = new Set<() => void>();

function subscribe(listener: () => void) {
  listeners.add(listener);
  const unsubscribe = () => {
    listeners.delete(listener);
  };
  return unsubscribe;
}

function getSnapshot() {
  return state;
}

function setState(next: Table) {
  state = next;
  for (const notify of listeners) {
    notify();
  }
}

export default function TableView() {
  const table = useSyncExternalStore(subscribe, getSnapshot);

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8000/ws_counters");
    ws.onmessage = (event) => setState(JSON.parse(event.data));
    return () => ws.close();
  }, []);

  return <pre>{JSON.stringify(table, null, 2)}</pre>;
}