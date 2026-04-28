import { useEffect, useState, useRef } from "react";
import { useLocation, useNavigate } from "react-router-dom";

export default function Loading() {
  const routerLocation = useLocation();
  const navigate = useNavigate();
  const hasCalledAPI = useRef(false);

  const [messageIndex, setMessageIndex] = useState(0);

  const messages = [
    "Finding the best restaurants for your taste",
    "Discovering must-visit attractions",
    "Planning your day-by-day itinerary",
    "Checking top-rated experiences nearby",
    "Optimizing your travel routes",
    "Balancing your trip within budget",
    "Curating the perfect travel plan",
    "Finalizing your personalized itinerary"
  ];

  // rotating messages
  useEffect(() => {
    const interval = setInterval(() => {
      setMessageIndex((prev) => (prev + 1) % messages.length);
    }, 1500);

    return () => clearInterval(interval);
  }, []);

  // API call
  useEffect(() => {
    if (!routerLocation.state) {
      navigate("/");
      return;
    }

    if (hasCalledAPI.current) return;
    hasCalledAPI.current = true;

    const callAPI = async () => {
      try {
        const res = await fetch("http://127.0.0.1:8000/plan-trip", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(routerLocation.state)
        });

        const data = await res.json();

        console.log("API RESPONSE:", data);

        // ❗ ONLY real failure
        if (!res.ok || data.error) {
          navigate("/result", { state: { error: true } });
          return;
        }

        const finalData = {
          ...data,
          user_location: routerLocation.state.location
        };

        localStorage.setItem("tripData", JSON.stringify(finalData));

        navigate("/result", { state: finalData });

      } catch (err) {
        console.error("API Error:", err);
        navigate("/result", { state: { error: true } });
      }
    };

    callAPI();
  }, [routerLocation, navigate]);

  return (
    <div className="loading-container">
      <h2 className="loading-text">{messages[messageIndex]}</h2>

      {/* SAME UI */}
      <div className="dots">
        <span></span>
        <span></span>
        <span></span>
      </div>
    </div>
  );
}