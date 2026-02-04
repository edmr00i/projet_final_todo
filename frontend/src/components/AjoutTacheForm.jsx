import React, { useState } from "react";

function AjoutTacheForm({ onAjoutTache }) {
  const [titre, setTitre] = useState("");
  const [description, setDescription] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!titre.trim()) return;

    await onAjoutTache(titre, description);
    setTitre("");
    setDescription("");
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={titre}
        onChange={(e) => setTitre(e.target.value)}
        placeholder="Ajouter une nouvelle tâche"
      />
      <textarea
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        placeholder="Description (optionnel)"
      />
      <button type="submit">Ajouter</button>
    </form>
  );
}

export default AjoutTacheForm;
