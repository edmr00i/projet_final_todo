import React, { useState } from "react";

function TacheItem({ tache, onSupprimeTache, onToggleTache, onUpdateTache }) {
  const [editing, setEditing] = useState(false);
  const [titre, setTitre] = useState(tache.titre);
  const [description, setDescription] = useState(tache.description ?? "");
  const [termine, setTermine] = useState(tache.termine);

  const handleSave = async () => {
    const t = titre.trim();
    if (!t) return;
    try {
      await onUpdateTache(tache.id, { titre: t, description, termine });
      setEditing(false);
    } catch (err) {
      console.error(err);
    }
  };

  const handleCancel = () => {
    setTitre(tache.titre);
    setDescription(tache.description ?? "");
    setTermine(tache.termine);
    setEditing(false);
  };

  const handleToggle = () => {
    onToggleTache(tache.id, tache.termine);
  };

  if (editing) {
    return (
      <li className="tache-card tache-card--editing">
        <div className="tache-card__body">
          <input
            type="text"
            className="input input--title"
            value={titre}
            onChange={(e) => setTitre(e.target.value)}
            placeholder="Titre"
          />
          <textarea
            className="input input--description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Description (optionnel)"
            rows={3}
          />
          <label className="checkbox-label">
            <input
              type="checkbox"
              checked={!!termine}
              onChange={(e) => setTermine(e.target.checked)}
            />
            <span>Terminée</span>
          </label>
        </div>
        <div className="tache-card__actions">
          <button type="button" className="btn btn--primary" onClick={handleSave}>
            Enregistrer
          </button>
          <button type="button" className="btn btn--secondary" onClick={handleCancel}>
            Annuler
          </button>
        </div>
      </li>
    );
  }

  return (
    <li className={`tache-card ${tache.termine ? "tache-card--done" : ""}`}>
      <div className="tache-card__body">
        <h4 className="tache-card__titre">{tache.titre}</h4>
        {tache.description ? (
          <p className="tache-card__description">{tache.description}</p>
        ) : null}
        <div className="tache-card__meta">
          <span className="tache-card__statut">
            {tache.termine ? "Terminée" : "En cours"}
          </span>
        </div>
      </div>
      <div className="tache-card__actions">
        <label className="checkbox-label checkbox-label--inline">
          <input
            type="checkbox"
            checked={!!tache.termine}
            onChange={handleToggle}
          />
          <span>Terminée</span>
        </label>
        <button
          type="button"
          className="btn btn--secondary btn--small"
          onClick={() => setEditing(true)}
        >
          Modifier
        </button>
        <button
          type="button"
          className="btn btn--danger btn--small"
          onClick={() => onSupprimeTache(tache.id)}
        >
          Supprimer
        </button>
      </div>
    </li>
  );
}

export default TacheItem;
