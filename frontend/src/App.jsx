import React, { useState, useEffect } from "react";
import TacheListe from "./components/TacheListe";
import AjoutTacheForm from "./components/AjoutTacheForm";
import {
  fetchTachesApi,
  createTacheApi,
  deleteTacheApi,
  toggleTacheApi,
} from "./api";
function App() {
  const [taches, setTaches] = useState([]);
  const [erreur, setErreur] = useState(null);

  const handleAjoutTache = async (titre, description) => {
    try {
      const nouvelleTache = await createTacheApi(titre, description);
      setTaches((prevTaches) => [...prevTaches, nouvelleTache]);
    } catch (error) {
      console.error("Erreur lors de l'ajout de la tâche :", error);
      setErreur(error.message);
    }
  };

  const handleSupprimeTache = async (id) => {
    try {
      await deleteTacheApi(id);
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
      const tacheMiseAJour = await toggleTacheApi(id, termineActuel);

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

  useEffect(() => {
    const fetchTaches = async () => {
      try {
        const data = await fetchTachesApi();
        console.log("Données reçues de Django :", data);
        setTaches(data);
      } catch (error) {
        console.error("Erreur Fetch :", error);
        setErreur(error.message);
      }
    };

    fetchTaches();
  }, []);

  return (
    <div>
      <AjoutTacheForm onAjoutTache={handleAjoutTache} />
      <h1>Ma Liste de Tâches</h1>
      <TacheListe
        taches={taches}
        erreur={erreur}
        onSupprimeTache={handleSupprimeTache}
        onToggleTache={handleToggleTache}
      />
    </div>
  );
}

export default App;
