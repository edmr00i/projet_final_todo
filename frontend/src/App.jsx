import React, { useState, useEffect } from "react";
import "./App.css";
import TacheListe from "./components/TacheListe";
import AjoutTacheForm from "./components/AjoutTacheForm";
import LoginPage from "./components/LoginPage";
import {
  fetchTachesApi,
  createTacheApi,
  deleteTacheApi,
  toggleTacheApi,
  updateTacheApi,
  loginApi,
} from "./api";
function App() {
  const [token, setToken] = useState(() => localStorage.getItem("token"));
  const [taches, setTaches] = useState([]);
  const [erreur, setErreur] = useState(null);



  const handleLogout = () => {
    localStorage.removeItem("token");
    setToken(null);
  };
  
  const handleLogin = async (username, password) => {
    try {
      const data = await loginApi(username, password);
      const newToken = data.token;
      localStorage.setItem("token", newToken);
      setToken(newToken);
    } catch (error) {
      console.error("Erreur lors de la connexion :", error);
      setErreur(error.message);
    }
  };

  const handleAjoutTache = async (titre, description) => {
    try {
      const nouvelleTache = await createTacheApi(titre, description, token);
      setTaches((prevTaches) => [...prevTaches, nouvelleTache]);
    } catch (error) {
      console.error("Erreur lors de l'ajout de la tâche :", error);
      setErreur(error.message);
    }
  };

  const handleSupprimeTache = async (id) => {
    try {
      await deleteTacheApi(id, token);
      setTaches((prevTaches) =>
        prevTaches.filter((tache) => tache.id !== id)
      );
    } catch (error) {
      console.error("Erreur lors de la suppression de la tâche :", error);
      setErreur(error.message);
    }
  };

  const handleToggleTache = async (id, termineActuel) => {
    try {
      const tacheMiseAJour = await toggleTacheApi(id, termineActuel, token);

      setTaches((prevTaches) =>
        prevTaches.map((tache) =>
          tache.id === id ? { ...tache, ...tacheMiseAJour } : tache
        )
      );
    } catch (error) {
      console.error("Erreur lors de la mise à jour de la tâche :", error);
      setErreur(error.message);
    }
  };

  const handleUpdateTache = async (id, data) => {
    try {
      const tacheMiseAJour = await updateTacheApi(id, data, token);
      setTaches((prevTaches) =>
        prevTaches.map((tache) =>
          tache.id === id ? { ...tache, ...tacheMiseAJour } : tache
        )
      );
    } catch (error) {
      console.error("Erreur lors de la modification de la tâche :", error);
      setErreur(error.message);
    }
  };

  useEffect(() => {
    if (!token) return;
    const fetchTaches = async () => {
      try {
        const data = await fetchTachesApi(token);
        setTaches(data);
      } catch (error) {
        console.error("Erreur Fetch :", error);
        setErreur(error.message);
      }
    };

    fetchTaches();
  }, [token]);

  if (!token) {
    return (
      <div className="app">
        <LoginPage onSubmit={handleLogin} />
      </div>
    );
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1 className="app-title">Ma Liste de Tâches</h1>
        <button type="button" className="btn btn--secondary" onClick={handleLogout}>
          Déconnexion
        </button>
      </header>
      <main className="app-main">
        <AjoutTacheForm onAjoutTache={handleAjoutTache} />
        <TacheListe
          taches={taches}
          erreur={erreur}
          onSupprimeTache={handleSupprimeTache}
          onToggleTache={handleToggleTache}
          onUpdateTache={handleUpdateTache}
        />
      </main>
    </div>
  );
}

export default App;
