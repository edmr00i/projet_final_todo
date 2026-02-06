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
  startReportGenerationApi,
  checkTaskStatusApi,
} from "./api";
function App() {
  const [token, setToken] = useState(() => localStorage.getItem("token"));
  const [taches, setTaches] = useState([]);
  const [erreur, setErreur] = useState(null);
  const [reportTaskId, setReportTaskId] = useState(null);
  const [reportStatus, setReportStatus] = useState("");



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
      console.error("Erreur lors de l'ajout de la tÃ¢che :", error);
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
      console.error("Erreur lors de la suppression de la tÃ¢che :", error);
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
      console.error("Erreur lors de la mise Ã  jour de la tÃ¢che :", error);
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
      console.error("Erreur lors de la modification de la tÃ¢che :", error);
      setErreur(error.message);
    }
  };

  const handleGenerateReport = async () => {
    try {
      setReportStatus("Démarrage de la génération du rapport...");
      const data = await startReportGenerationApi(token);
      setReportTaskId(data.task_id);
      setReportStatus(`Rapport en cours de génération (ID: ${data.task_id})`);
    } catch (error) {
      console.error("Erreur lors du démarrage du rapport :", error);
      setErreur(error.message);
      setReportStatus("Erreur lors du démarrage de la génération du rapport");
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

  useEffect(() => {
    if (!reportTaskId) return;

    const interval = setInterval(async () => {
      try {
        const statusData = await checkTaskStatusApi(reportTaskId, token);
        
        // Mettre à jour le statut selon l'état de la tâche
        if (statusData.state === "PENDING") {
          setReportStatus(`Rapport en attente... (${statusData.state})`);
        } else if (statusData.state === "STARTED") {
          setReportStatus(`Génération en cours... (${statusData.state})`);
        } else if (statusData.state === "SUCCESS") {
          setReportStatus(statusData.result);
          clearInterval(interval);
        } else if (statusData.state === "FAILURE") {
          setReportStatus(`Erreur: ${statusData.result}`);
          clearInterval(interval);
        } else {
          setReportStatus(`Statut: ${statusData.state}`);
        }
      } catch (error) {
        console.error("Erreur lors de la vérification du statut :", error);
        setReportStatus("Erreur lors de la vérification du statut");
        clearInterval(interval);
      }
    }, 3000); // Vérifier toutes les 3 secondes

    // Nettoyer l'intervalle quand le composant se démonte ou quand reportTaskId change
    return () => clearInterval(interval);
  }, [reportTaskId, token]);

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
        <div className="app-header__actions">
          <button 
            type="button" 
            className="btn btn--primary" 
            onClick={handleGenerateReport}
            disabled={!!reportTaskId && reportStatus.includes("en cours")}
          >
            Générer un Rapport
          </button>
          <button type="button" className="btn btn--secondary" onClick={handleLogout}>
            Déconnexion
          </button>
        </div>
      </header>
      {reportStatus && (
        <div className={`report-status ${
          reportStatus.toLowerCase().includes('erreur') ? 'report-status--error' :
          reportStatus.toLowerCase().includes('succès') || reportStatus.includes('SUCCESS') ? 'report-status--success' :
          'report-status--pending'
        }`}>
          <strong>Statut du rapport :</strong> {reportStatus}
        </div>
      )}
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