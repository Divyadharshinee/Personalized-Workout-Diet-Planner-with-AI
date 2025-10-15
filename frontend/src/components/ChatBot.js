import React, {useState} from "react";
import { sendChat } from "../api";

export default function ChatBot(){
  const [msg, setMsg] = useState("");
  const [history, setHistory] = useState([]);

  const send = async ()=>{
    if(!msg) return;
    const entry = {from:"user", text:msg};
    setHistory(h=>[...h, entry]);
    setMsg("");
    const res = await sendChat(msg);
    const reply = res.reply || JSON.stringify(res);
    setHistory(h=>[...h, {from:"bot", text:reply}]);
  };

  return (
    <div className="card">
      <h3>Health Insights (AI)</h3>
      <div style={{minHeight:120, border:"1px solid #eee", padding:8, borderRadius:6, overflowY:"auto"}}>
        {history.map((h,i)=>(
          <div key={i} style={{textAlign: h.from==="user"?"right":"left", margin:"6px 0"}}>
            <div style={{display:"inline-block", background: h.from==="user"?"#dcf8c6":"#f1f1f1", padding:8, borderRadius:6}}>
              {h.text}
            </div>
          </div>
        ))}
      </div>
      <textarea value={msg} onChange={e=>setMsg(e.target.value)} rows={3} />
      <button onClick={send}>Send</button>
    </div>
  );
}
