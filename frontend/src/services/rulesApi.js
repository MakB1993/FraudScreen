const BASE_URL = import.meta.env.VITE_API_BASE_URL;

export async function getRules() {
  const response = await fetch(`${BASE_URL}/rules`);

  if (!response.ok) {
    throw new Error(
      `Failed to fetch rules: HTTP ${response.status}`
    );
  }

  return await response.json();
}

export async function updateRule(ruleKey, editForm) {
  const response = await fetch(
    `${BASE_URL}/rules/${ruleKey}`,
    {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(editForm),
    }
  );

  if (!response.ok) {
    const errorData = await response.json();

    throw new Error(
      errorData.detail || `HTTP ${response.status}`
    );
  }

  return response.json();
}