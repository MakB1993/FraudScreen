const BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  "http://127.0.0.1:8000";
export async function getFraudEvaluations(
  limit = 10,
  offset = 0,
  filters = {}
) {
  const params = new URLSearchParams({
    limit: limit.toString(),
    offset: offset.toString(),
  });

  if (filters.decision) {
    params.append("decision", filters.decision);
  }

  if (filters.min_score) {
    params.append("min_score", filters.min_score);
  }

  if (filters.max_score) {
    params.append("max_score", filters.max_score);
  }

  const response = await fetch(
    `${BASE_URL}/fraud-evaluations?${params.toString()}`
  );

  if (!response.ok) {
    throw new Error("Failed to load fraud evaluations");
  }

  return response.json();
}

export async function getFraudEvaluationById(id) {
  const response = await fetch(
    `${BASE_URL}/fraud-evaluations/${id}`
  );

  if (!response.ok) {
    throw new Error("Failed to load fraud evaluation");
  }

  return response.json();
}

