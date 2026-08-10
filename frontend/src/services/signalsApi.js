const BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

export async function getSignals() {
  const response = await fetch(`${BASE_URL}/signals`);

  if (!response.ok) {
    throw new Error("Failed to load signals");
  }

  return response.json();
}