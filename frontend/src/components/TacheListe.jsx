import React from "react";
import TacheItem from "./TacheItem";

const TacheListe = ({ taches, erreur, onSupprimeTache, onToggleTache }) => {
  return (
    <div className="tache-container">
      <h3>Ma liste de tâches</h3>

      {erreur && <p style={{ color: "red" }}>{erreur}</p>}

      <ul>
        {taches && taches.length > 0 ? (
          taches.map((tache) => (
            <TacheItem
              key={tache.id}
              tache={tache}
              onSupprimeTache={onSupprimeTache}
              onToggleTache={onToggleTache}
            />
          ))
        ) : (
          !erreur && <p>Chargement des tâches...</p>
        )}
      </ul>
    </div>
  );
};

export default TacheListe;