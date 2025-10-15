import React, {useEffect, useState} from "react";
import { fetchProfile } from "../api";

export default function Dashboard(){
  const [profile, setProfile] = useState(null);
  useEffect(()=> {
    fetchProfile().then(setProfile);
  },[]);
  return (
    <div className="card">
      <h3>Dashboard</h3>
      {profile && profile.name ? (
        <div>
          <p><strong>{profile.name}</strong> — {profile.age} yrs — {profile.goals}</p>
          <p>Diet: {profile.dietary_pref} • Activity: {profile.activity_level}</p>
        </div>
      ) : <p>No profile yet. Please add your health profile.</p>}
      <p>Use the tabs to generate meal plans, analyze food images, or chat with the AI nutritionist.</p>
    </div>
  );
}
