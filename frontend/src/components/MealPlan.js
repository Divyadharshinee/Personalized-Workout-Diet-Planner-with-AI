import React, {useState, useEffect} from "react";
import { getMealPlan } from "../api";

export default function MealPlan(){
  const [plan, setPlan] = useState(null);
  useEffect(()=> {
    getMealPlan().then(setPlan);
  },[]);
  if(!plan) return <div className="card">Loading meal plan...</div>;
  return (
    <div className="card">
      <h3>7-Day Meal Plan</h3>
      <p>Shopping list:</p>
      <ul>
        {plan.shopping_list.map((s,i)=><li key={i}>{s}</li>)}
      </ul>
      <div>
        {plan.days.map((d,idx)=>(
          <div key={idx} className="meal-day">
            <strong>{d.day}</strong> — {d.calories_target} kcal
            <div>Macros: P {d.macros.protein_g}g • C {d.macros.carbs_g}g • F {d.macros.fat_g}g</div>
            <div>
              <em>Breakfast:</em> {d.meals.breakfast}<br/>
              <em>Lunch:</em> {d.meals.lunch}<br/>
              <em>Snack:</em> {d.meals.snack}<br/>
              <em>Dinner:</em> {d.meals.dinner}<br/>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
