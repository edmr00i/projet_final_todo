const API_BASE_URL = "http://127.0.0.1:8000/api";

export async function fetchTachesApi(token) {
  const response = await fetch(`${API_BASE_URL}/taches/`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Token ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error(
      `Erreur ${response.status}: Impossible de rÃ©cupÃ©rer les donnÃ©es`
    );
  }

  return response.json();
}

export async function loginApi(username, password) {
  const response = await fetch(`${API_BASE_URL}/token/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  if (!response.ok) {
    throw new Error("Identifiants incorrects");
  }
  return response.json();
}

export async function createTacheApi(titre, description, token) {
  const response = await fetch(`${API_BASE_URL}/taches/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Token ${token}`,
    },
    body: JSON.stringify({ titre, description }),
  });

  if (!response.ok) {
    throw new Error(
      `Erreur ${response.status}: Impossible de crÃ©er la tÃ¢che`
    );
  }

  return response.json();
}

export async function deleteTacheApi(id, token) {
  const response = await fetch(`${API_BASE_URL}/taches/${id}/`, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Token ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error(
      `Erreur ${response.status}: Impossible de supprimer la tÃ¢che`
    );
  }
}

export async function toggleTacheApi(id, termineActuel, token) {
  return updateTacheApi(id, { termine: !termineActuel }, token);
}

export async function updateTacheApi(id, data, token) {
  const response = await fetch(`${API_BASE_URL}/taches/${id}/`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Token ${token}`,
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error(
      `Erreur ${response.status}: Impossible de mettre Ã  jour la tÃ¢che`
    );
  }

  return response.json();
}

export async function startReportGenerationApi(token) {
  const response = await fetch(`${API_BASE_URL}/start-report/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Token ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error(
      `Erreur ${response.status}: Impossible de démarrer la génération du rapport`
    );
  }

  return response.json();
}

export async function checkTaskStatusApi(taskId, token) {
  const response = await fetch(`${API_BASE_URL}/check-report-status/${taskId}/`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Token ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error(
      `Erreur ${response.status}: Impossible de vérifier le statut de la tâche`
    );
  }

  return response.json();
}