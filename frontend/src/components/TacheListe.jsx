import React, { useState, useEffect } from 'react';

const TacheListe = () => {
  const [taches, setTaches] = useState([]);
  const [erreur, setErreur] = useState(null);

  useEffect(() => {
    const fetchTaches = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/api/taches/", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            // VERIFIE BIEN : "Token" ou "Bearer" selon ta config Django
            "Authorization": "Token 334191d8e0b8a34ee2b5c80afc036aa5896f97d3" 
          }
        });

        if (!response.ok) {
          throw new Error(`Erreur ${response.status}: Impossible de récupérer les données`);
        }

        const data = await response.json();
        console.log("Données reçues de Django :", data); // Pour vérifier dans la console du navigateur
        setTaches(data);
      } catch (error) {
        console.error("Erreur Fetch :", error);
        setErreur(error.message);
      }
    };

    fetchTaches();
  }, []);

  return (
    <div className="tache-container">
      <h3>Ma liste de tâches</h3>
      
      {erreur && <p style={{ color: 'red' }}>{erreur}</p>}

      <ul>
        {taches.length > 0 ? (
          taches.map((tache) => (
            <li key={tache.id} style={{ marginBottom: '10px' }}>
              <strong>{tache.titre}</strong> - {tache.termine ? "✅ Terminé" : "⏳ En cours"}
              <br />
              <small>{tache.description}</small>
            </li>
          ))
        ) : (
          !erreur && <p>Chargement des tâches...</p>
        )}
      </ul>
    </div>
  );
};

export default TacheListe;