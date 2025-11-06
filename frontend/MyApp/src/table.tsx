import { useEffect } from "react";
import { create } from "zustand";

type Table = Record<number, number>;

const useStore = create<{ table: Table; setTable: (t: Table) => void }>((set) => ({
  table: {},
  setTable: (t) => set({ table: t }),
}));

export default function App() {
  const { table, setTable } = useStore();

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8000/ws_counters");
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setTable(data);
    };
    return () => ws.close();
  }, [setTable]);

  return <pre>{JSON.stringify(table, null, 2)}</pre>;
}