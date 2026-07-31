const BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

export async function getTransactions(limit = 10, offset = 0) {
  const response = await fetch(
    `${BASE_URL}/transactions?limit=${limit}&offset=${offset}`
  );

  if (!response.ok) {
    throw new Error("Failed to load transactions");
  }

  return response.json();
}