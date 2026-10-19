import { useEffect, useState } from "react";

// nginx가 /api 를 backend 컨테이너로 프록시한다 (frontend/nginx.conf)
const API = "/api/todos";

async function request(url = API, options) {
  const res = await fetch(url, options);
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return res.status === 204 ? null : res.json();
}

const json = (method, body) => ({
  method,
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(body),
});

export default function App() {
  const [todos, setTodos] = useState([]);
  const [title, setTitle] = useState("");
  const [error, setError] = useState("");

  const run = async (action) => {
    try {
      setError("");
      await action();
      setTodos(await request());
    } catch (e) {
      setError(e.message);
    }
  };

  useEffect(() => {
    run(async () => {});
  }, []);

  const add = (e) => {
    e.preventDefault();
    if (!title.trim()) return;
    run(() => request(API, json("POST", { title })));
    setTitle("");
  };

  return (
    <main style={{ maxWidth: 480, margin: "40px auto", fontFamily: "sans-serif" }}>
      <h1>Todo</h1>
      <form onSubmit={add}>
        <input value={title} onChange={(e) => setTitle(e.target.value)} placeholder="할 일" />
        <button>추가</button>
      </form>
      {error && <p style={{ color: "crimson" }}>{error}</p>}
      <ul>
        {todos.map((t) => (
          <li key={t.id}>
            <input
              type="checkbox"
              checked={t.done}
              onChange={() =>
                run(() => request(`${API}/${t.id}`, json("PUT", { title: t.title, done: !t.done })))
              }
            />
            <span style={{ textDecoration: t.done ? "line-through" : "none" }}>{t.title}</span>
            <button onClick={() => run(() => request(`${API}/${t.id}`, { method: "DELETE" }))}>
              삭제
            </button>
          </li>
        ))}
      </ul>
    </main>
  );
}
