import React, { useState } from "react";
import "./Home.css"

export default function Home() {
  const [activeIndex, setActiveIndex] = useState(null);

  // Λειτουργία για εναλλαγή ενεργού στοιχείου
  const toggleForm = (index) => {
    setActiveIndex(activeIndex === index ? null : index);
  };

  return (
    <div className="list">
      {["Επιλογή 1", "Επιλογή 2", "Επιλογή 3"].map((title, index) => (
        <div key={index} className="item">
          <div className="title" onClick={() => toggleForm(index)}>
            {title}
          </div>
          {activeIndex === index && (
            <div className="form">
              <form>
                <label>Όνομα:</label>
                <input type="text" />
                <label>Email:</label>
                <input type="email" />
                <button type="submit">Υποβολή</button>
              </form>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
