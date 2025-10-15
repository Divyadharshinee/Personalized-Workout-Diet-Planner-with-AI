import React, {useState, useEffect} from "react";
import { fetchProfile, saveProfile } from "../api";

export default function ProfileForm(){
  const [form, setForm] = useState({
    name:"", age:20, gender:"female", height_cm:165, weight_kg:60,
    activity_level:"moderate", dietary_pref:"mixed", allergies:"", budget:"medium", region:"", goals:""
  });
  useEffect(()=> {
    fetchProfile().then(data => {
      if(data && data.name) setForm({...form, ...data});
    });
    // eslint-disable-next-line
  },[]);

  const handleChange = (k,v) => setForm({...form,[k]:v});
  const save = async () => {
    await saveProfile(form);
    alert("Profile saved.");
  };
  return (
    <div className="card">
      <h3>Health Profile</h3>
      <label>Name</label>
      <input value={form.name} onChange={e=>handleChange("name", e.target.value)} />
      <label>Age</label>
      <input type="number" value={form.age} onChange={e=>handleChange("age", e.target.value)} />
      <label>Gender</label>
      <select value={form.gender} onChange={e=>handleChange("gender", e.target.value)}>
        <option>female</option>
        <option>male</option>
        <option>other</option>
      </select>
      <label>Height (cm)</label>
      <input type="number" value={form.height_cm} onChange={e=>handleChange("height_cm", e.target.value)} />
      <label>Weight (kg)</label>
      <input type="number" value={form.weight_kg} onChange={e=>handleChange("weight_kg", e.target.value)} />
      <label>Activity level</label>
      <select value={form.activity_level} onChange={e=>handleChange("activity_level", e.target.value)}>
        <option value="sedentary">sedentary</option>
        <option value="light">light</option>
        <option value="moderate">moderate</option>
        <option value="active">active</option>
      </select>
      <label>Dietary Preference</label>
      <select value={form.dietary_pref} onChange={e=>handleChange("dietary_pref", e.target.value)}>
        <option value="mixed">Mixed</option>
        <option value="vegetarian">Vegetarian</option>
        <option value="non-veg">Non-Veg</option>
      </select>
      <label>Allergies (comma separated)</label>
      <input value={form.allergies} onChange={e=>handleChange("allergies", e.target.value)} />
      <label>Budget (low/medium/high)</label>
      <input value={form.budget} onChange={e=>handleChange("budget", e.target.value)} />
      <label>Region / cultural food habits</label>
      <input value={form.region} onChange={e=>handleChange("region", e.target.value)} />
      <label>Goals (e.g., lose weight, gain muscle)</label>
      <input value={form.goals} onChange={e=>handleChange("goals", e.target.value)} />
      <button onClick={save}>Save Profile</button>
    </div>
  );
}
