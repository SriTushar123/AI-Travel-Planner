import { useNavigate } from "react-router-dom";

export default function Home() {
  const navigate = useNavigate();

  return (
    <div className="home-container">

      {/* LEFT IMAGE */}
      <div className="home-left">
        <img
          src="https://images.unsplash.com/photo-1501785888041-af3ef285b470"
          alt="travel"
        />
      </div>

      {/* RIGHT CONTENT */}
      <div className="home-right">
        <h1>Your Complete Travel Itinerary</h1>
        <p>Plan your dream trip in seconds with AI</p>

        <button onClick={() => navigate("/planner")}>
          LET’S GO ✈️
        </button>
      </div>

    </div>
  );
}