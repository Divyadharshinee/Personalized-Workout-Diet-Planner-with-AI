const BASE = process.env.REACT_APP_API_BASE || "http://localhost:5000/api";



export async function fetchProfile() {
  const r = await fetch(`${BASE}/profile`);
  return r.json();
}
export async function saveProfile(data) {
  const r = await fetch(`${BASE}/profile`, {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify(data)
  });
  return r.json();
}
export async function getMealPlan() {
  const r = await fetch(`${BASE}/mealplan`);
  return r.json();
}
export async function uploadImage(file) {
  const fd = new FormData();
  fd.append("image", file);
  const r = await fetch(`${BASE}/analyze_image`, { method: "POST", body: fd });
  return r.json();
}
export async function sendChat(message) {
  const r = await fetch(`${BASE}/chat`, {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({message})
  });
  return r.json();
}
