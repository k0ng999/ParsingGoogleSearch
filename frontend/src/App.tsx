import { useState } from "react";

export default function App() {
  const [keyword, setKeyword] = useState<string>("");
  const [siteName, setSiteName] = useState<string>("");
  const [result, setResult] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setResult(null);
    setError(null);
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/google-rank/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ keyword, site_name: siteName }),
      });

      const data = await response.json();
      if (response.ok) {
        setResult(data.result);
      } else {
        setError(data.error);
      }
    } catch (err) {
      setError("Ошибка при отправке запроса");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        margin: "0 auto",
        textAlign: "center",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        flexDirection: "column",
      }}
    >
      <h1>Поиск позиции сайта в Google</h1>
      <form
        onSubmit={handleSubmit}
        style={{ display: "flex", flexDirection: "column", gap: "10px" }}
      >
        <input
          type="text"
          placeholder="Введите ключевое слово"
          value={keyword}
          onChange={(e) => setKeyword(e.target.value)}
          required
          style={{ padding: "8px", fontSize: "16px" }}
        />
        <input
          type="text"
          placeholder="Введите имя сайта"
          value={siteName}
          onChange={(e) => setSiteName(e.target.value)}
          required
          style={{ padding: "8px", fontSize: "16px" }}
        />
        <button
          type="submit"
          disabled={loading}
          style={{ padding: "10px", fontSize: "16px", cursor: "pointer" }}
        >
          {loading ? "Ищем..." : "Найти позицию"}
        </button>
      </form>

      {result !== null && (
        <p>
          Результат: <strong>{result}</strong>
        </p>
      )}
      {error && <p style={{ color: "red" }}>Ошибка: {error}</p>}
    </div>
  );
}
