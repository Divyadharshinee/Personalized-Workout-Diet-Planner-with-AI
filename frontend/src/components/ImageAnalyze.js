import React, {useState} from "react";
import { uploadImage } from "../api";

export default function ImageAnalyze(){
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const submit = async ()=>{
    if(!file) return alert("Choose an image first");
    setLoading(true);
    const r = await uploadImage(file);
    setResult(r);
    setLoading(false);
  };

  return (
    <div className="card">
      <h3>Upload Food Image</h3>
      <input type="file" accept="image/*" onChange={e=>setFile(e.target.files[0])} />
      <button onClick={submit} disabled={loading}>{loading? "Analyzing...":"Analyze"}</button>
      {result && (
        <div style={{marginTop:12}}>
          <h4>Analysis</h4>
          <pre style={{whiteSpace:"pre-wrap"}}>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
