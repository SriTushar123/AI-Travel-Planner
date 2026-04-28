import { useLocation, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";

export default function Result() {
  const routerLocation = useLocation();
  const navigate = useNavigate();

  const [data, setData] = useState(routerLocation.state || null);

  useEffect(() => {
    if (!routerLocation.state) {
      const saved = localStorage.getItem("tripData");
      if (saved) setData(JSON.parse(saved));
    }
  }, []);

  // ❌ Error UI (unchanged)
  if (data?.error) {
    return (
      <div className="result-page">
        <h2>⚠️ Oops, something went wrong 😔</h2>
        <button onClick={() => navigate("/")}>Try Again</button>
      </div>
    );
  }

  if (!data) return null;

  // ⭐ Rating helper
  const renderStars = (rating) => {
    if (!rating) return "";
    return "⭐".repeat(Math.round(rating));
  };

  return (
    <div className="result-page">

      {/* HERO */}
      <div className="hero">
        <img
          src="https://images.unsplash.com/photo-1507525428034-b723cf961d3e"
          alt="travel"
        />
        <h1>{data.user_location || "Your Trip"} ✈️</h1>
      </div>

      {/* OVERVIEW */}
      <div className="overview-card">
        <h2>🌍 Overview</h2>
        <p>{data.destination_overview || "No overview available"}</p>
      </div>

      {/* BUDGET */}
      <div className="budget-card" style={{ marginBottom: "30px" }}>
        <h2>💰 Budget Breakdown</h2>
        <ul>
          <li>Total: ₹{data.budget?.total ?? "-"}</li>
          <li>Stay: ₹{data.budget?.accommodation ?? "-"}</li>
          <li>Food: ₹{data.budget?.food ?? "-"}</li>
          <li>Transport: ₹{data.budget?.transport ?? "-"}</li>
          <li>Activities: ₹{data.budget?.activities ?? "-"}</li>
          <li>Misc: ₹{data.budget?.misc ?? "-"}</li>
        </ul>
      </div>

      {/* ITINERARY */}
      <div className="days-container">
        {data.itinerary?.length > 0 ? (
          data.itinerary.map((day) => (
            <div className="day-card" key={day.day}>
              <h3>
                📅 Day {day.day} - {day.date || ""} ({day.city || ""})
              </h3>

              <p>
                🌡 {day.weather?.min_temp_c ?? "-"}°C - {day.weather?.max_temp_c ?? "-"}°C
              </p>

              <ul>

                {/* 🌅 MORNING */}
                <li>
                  <strong>🌅 Morning</strong>
                  <div>{day.morning?.acitivity || "Not available"}</div>
                  <div>{day.morning?.description || ""}</div>
                  <div>{renderStars(day.morning?.rating)}</div>
                </li>

                {/* 🌇 AFTERNOON */}
                <li>
                  <strong>🌇 Afternoon</strong>
                  <div>{day.afternoon?.acitivity || "Not available"}</div>
                  <div>{day.afternoon?.description || ""}</div>
                  <div>{renderStars(day.afternoon?.rating)}</div>
                </li>

                {/* 🌙 EVENING */}
                <li>
                  <strong>🌙 Evening</strong>
                  <div>{day.evening?.acitivity || "Not available"}</div>
                  <div>{day.evening?.description || ""}</div>
                  <div>{renderStars(day.evening?.rating)}</div>
                </li>

              </ul>
            </div>
          ))
        ) : (
          <p>No itinerary available.</p>
        )}
      </div>

      {/* 🚗 TRANSPORTATION */}
      <div className="overview-card">
        <h2>🚗 Transportation</h2>
        <ul>
          {data.transporatation?.modes_of_transportation?.length > 0 ? (
            data.transporatation.modes_of_transportation.map((item, index) => (
              <li key={index}>{item}</li>
            ))
          ) : (
            <li>No transportation data available</li>
          )}
        </ul>
      </div>

      {/* 🎉 END */}
      <div className="overview-card">
        <h2>🎉 Hurray! Your Trip is Ready!</h2>
      </div>

      {/* 🔁 PLAN ANOTHER TRIP BUTTON (RESTORED) */}
      <div style={{ textAlign: "center", margin: "30px 0" }}>
        <button onClick={() => navigate("/planner")}>
          Plan Another Trip ✈️
        </button>
      </div>

    </div>
  );
}