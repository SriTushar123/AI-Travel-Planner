import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Planner() {
  const navigate = useNavigate();

  const [destination, setDestination] = useState("");
  const [date, setDate] = useState("");
  const [budget, setBudget] = useState("");
  const [days, setDays] = useState("");

  const handleSubmit = () => {
    if (!destination || !date || !budget || !days) {
      alert("Please fill all fields");
      return;
    }

    navigate("/loading", {
      state: {
        location: destination,
        start_date: date,
        budget: Number(budget),
        days: Number(days)
      }
    });
  };

  return (
    <div className="planner-page">
      <div className="planner-card">
        <h1>Plan Your Trip ✈️</h1>

        <div className="input-group">
          <label>📍 Destination</label>
          <input
            type="text"
            placeholder="Where do you want to go?"
            value={destination}
            onChange={(e) => setDestination(e.target.value)}
          />
        </div>

        <div className="input-group">
          <label>📅 Start Date</label>
          <input
            type="date"
            value={date}
            min={new Date().toISOString().split("T")[0]}
            onChange={(e) => setDate(e.target.value)}
          />
        </div>

        <div className="input-group">
          <label>💰 Budget</label>
          <input
            type="number"
            placeholder="Enter your budget"
            value={budget}
            onChange={(e) => setBudget(e.target.value)}
          />
        </div>

        <div className="input-group">
          <label>🗓️ Number of Days</label>
          <select value={days} onChange={(e) => setDays(e.target.value)}>
            <option value="">Select days</option>
            {[1,2,3,4,5,6,7].map(d => (
              <option key={d} value={d}>{d} Days</option>
            ))}
          </select>
        </div>

        <button className="plan-btn" onClick={handleSubmit}>
          Create Itinerary 🚀
        </button>
      </div>
    </div>
  );
}