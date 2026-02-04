const API_BASE_URL = "http://127.0.0.1:8000/api/taches/";
const AUTH_HEADER = "Token 334191d8e0b8a34ee2b5c80afc036aa5896f97d3";

export async function fetchTachesApi() {
  const response = await fetch(API_BASE_URL, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: AUTH_HEADER,
    },
  });

  if (!response.ok) {
    throw new Error(
      `Erreur ${response.status}: Impossible de récupérer les données`
    );
  }

  return response.json();
}

export async function createTacheApi(titre, description) {
  const response = await fetch(API_BASE_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: AUTH_HEADER,
    },
    body: JSON.stringify({ titre, description }),
  });

  if (!response.ok) {
    throw new Error(
      `Erreur ${response.status}: Impossible de créer la tâche`
    );
  }

  return response.json();
}

export async function deleteTacheApi(id) {
  const response = await fetch(`${API_BASE_URL}${id}/`, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
      Authorization: AUTH_HEADER,
    },
  });

  if (!response.ok) {
    throw new Error(
      `Erreur ${response.status}: Impossible de supprimer la tâche`
    );
  }
}

export async function toggleTacheApi(id, termineActuel) {
  const response = await fetch(`${API_BASE_URL}${id}/`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      Authorization: AUTH_HEADER,
    },
    body: JSON.stringify({ termine: !termineActuel }),
  });

  if (!response.ok) {
    throw new Error(
      `Erreur ${response.status}: Impossible de mettre à jour la tâche`
    );
  }

  return response.json();
}

