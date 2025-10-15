import React, { useState, useEffect } from "react";
import ProfileForm from "./components/ProfileForm";
import MealPlan from "./components/MealPlan";
import ImageAnalyze from "./components/ImageAnalyze";
import ChatBot from "./components/ChatBot";
import Dashboard from "./components/Dashboard";

function App(){
  const [page, setPage] = useState("dashboard");
  return (
    <div className="container">
      <header>
        <h2>Personalized Workout & Diet Planner</h2>
        <nav>
          <button onClick={()=>setPage("dashboard")}>Dashboard</button>
          <button onClick={()=>setPage("profile")}>Profile</button>
          <button onClick={()=>setPage("mealplan")}>Meal Plan</button>
          <button onClick={()=>setPage("analyze")}>Analyze Food</button>
          <button onClick={()=>setPage("chat")}>Health Insights</button>
        </nav>
      </header>

      <main style={{marginTop:16}}>
        {page === "dashboard" && <Dashboard />}
        {page === "profile" && <ProfileForm />}
        {page === "mealplan" && <MealPlan />}
        {page === "analyze" && <ImageAnalyze />}
        {page === "chat" && <ChatBot />}
      </main>
    </div>
  );
}

export default App;
