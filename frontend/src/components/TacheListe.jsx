import React from "react";
import TacheItem from "./TacheItem";

const TacheListe = ({ taches, erreur, onSupprimeTache, onToggleTache, onUpdateTache }) => {
  return (
    <div className="tache-container">
      {erreur && <p className="message message--error">{erreur}</p>}

      <ul className="tache-list">
        {taches && taches.length > 0 ? (
          taches.map((tache) => (
            <TacheItem
              key={tache.id}
              tache={tache}
              onSupprimeTache={onSupprimeTache}
              onToggleTache={onToggleTache}
              onUpdateTache={onUpdateTache}
            />
          ))
        ) : (
          !erreur && <p className="message message--muted">Chargement des tâches...</p>
        )}
      </ul>
    </div>
  );
};

export default TacheListe;