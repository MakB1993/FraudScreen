const BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

export async function getTransactions(
  limit = 10,
  offset = 0,
  filters = {}
) {
  const params = new URLSearchParams({
    limit: limit.toString(),
    offset: offset.toString(),
  });

  if (filters.transaction_id) {
    params.append("transaction_id", filters.transaction_id);
  }

  if (filters.customer_id) {
    params.append("customer_id", filters.customer_id);
  }

  if (filters.email) {
    params.append("email", filters.email);
  }

  if (filters.ip_address) {
    params.append("ip_address", filters.ip_address);
  }

  if (filters.device_id) {
    params.append("device_id", filters.device_id);
  }

  if (filters.min_amount) {
    params.append("min_amount", filters.min_amount);
  }

  if (filters.max_amount) {
    params.append("max_amount", filters.max_amount);
  }

  if (filters.currency) {
    params.append("currency", filters.currency);
  }

  if (filters.start_date) {
    params.append("start_date", filters.start_date);
  }

  if (filters.end_date) {
    params.append("end_date", filters.end_date);
  }

  const response = await fetch(
    `${BASE_URL}/transactions?${params.toString()}`
  );

  if (!response.ok) {
    throw new Error("Failed to load transactions");
  }

  return response.json();
}

export async function getTransactionFraudEvaluation(transactionId) {
  const response = await fetch(
    `${BASE_URL}/transactions/${transactionId}/fraud-evaluation`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch fraud evaluation");
  }

  return response.json();
}