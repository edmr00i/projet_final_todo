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
    <form className="add-form" onSubmit={handleSubmit}>
      <input
        type="text"
        className="input input--title"
        value={titre}
        onChange={(e) => setTitre(e.target.value)}
        placeholder="Ajouter une nouvelle tâche"
      />
      <textarea
        className="input input--description"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        placeholder="Description (optionnel)"
        rows={2}
      />
      <button type="submit" className="btn btn--primary">
        Ajouter
      </button>
    </form>
  );
}

export default AjoutTacheForm;
