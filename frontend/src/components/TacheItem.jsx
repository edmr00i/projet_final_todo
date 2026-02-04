import React from "react";

function TacheItem({ tache, onSupprimeTache, onToggleTache }) {
  const handleClickSupprimer = () => {
    onSupprimeTache(tache.id);
  };

  const handleChangeTermine = () => {
    onToggleTache(tache.id, tache.termine);
  };

  return (
    <li>
      {" "}
      {tache.titre}{" "}
      <input
        type="checkbox"
        checked={!!tache.termine}
        onChange={handleChangeTermine}
      />
      <button type="button" onClick={handleClickSupprimer}>
        Supprimer
      </button>
    </li>
  );
}

export default TacheItem;
