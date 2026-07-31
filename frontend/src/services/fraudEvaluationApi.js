const BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  "http://127.0.0.1:8000";

export async function getFraudEvaluation(transactionId) {
  const response = await fetch(
    `${BASE_URL}/transactions/${transactionId}/fraud-evaluation`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch fraud evaluation");
  }

  return response.json();
}