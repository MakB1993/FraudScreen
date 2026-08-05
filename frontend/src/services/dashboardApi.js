const BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";


export async function getDashboardSummary() {
  const response = await fetch(
    `${BASE_URL}/dashboard/summary`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch dashboard summary");
  }

  return response.json();
}

export async function getTransactionsOverTime() {
  const response = await fetch(
    "http://127.0.0.1:8000/dashboard/transactions-over-time"
  );

  if (!response.ok) {
    throw new Error("Failed to fetch transactions over time");
  }

  return response.json();
}