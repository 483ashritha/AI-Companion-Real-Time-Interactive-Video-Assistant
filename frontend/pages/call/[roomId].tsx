import { useRouter } from 'next/router';
import { useEffect, useRef, useState } from 'react';
import { useWebRTC } from '../../hooks/useWebRTC';
const BACKEND = process.env.NEXT_PUBLIC_BACKEND || 'http://localhost:8000';
export default function CallPage(){
  const router = useRouter(); const { roomId } = router.query;
  const [userId] = useState('u-'+Math.random().toString(36).slice(2,6));
  const { startLocal, connectSocket, createPC, createOffer, sendChat, stop, localStream, remoteStream, toggleMic, toggleCam } = useWebRTC(BACKEND);
  const localRef = useRef<HTMLVideoElement|null>(null); const remoteRef = useRef<HTMLVideoElement|null>(null);
  const [messages, setMessages] = useState<any[]>([]); const [chatText, setChatText] = useState('');
  useEffect(()=>{ if(!roomId) return; (async ()=>{ try{ await startLocal(); }catch(e){ console.warn('media error', e); } })(); },[roomId]);
  useEffect(()=> { if(localRef.current && localStream) localRef.current.srcObject = localStream; }, [localStream]);
  useEffect(()=> { if(remoteRef.current && remoteStream) remoteRef.current.srcObject = remoteStream; }, [remoteStream]);
  function onEvent(ev:string,payload:any){ if(ev==='chat') setMessages(prev=>[...prev,{from:payload.from||'peer', text:payload.text}]); }
  async function startAsUser(){ connectSocket(roomId as string, userId, onEvent); await createPC(); await createOffer(roomId as string); }
  async function startAsCompanion(){ connectSocket(roomId as string, userId, onEvent); await createPC(); }
  function send(){ if(!chatText) return; sendChat(chatText); setMessages(prev=>[...prev,{from:'me', text:chatText}]); setChatText(''); }
  return (
    <div className='container'>
      <h2 className='text-2xl font-semibold text-indigo-600'>Call room: {roomId}</h2>
      <div className='grid grid-cols-2 gap-4 mt-4'>
        <div className='card'>
          <video ref={localRef} className='w-full h-64 bg-black rounded' autoPlay muted playsInline />
          <div className='mt-2 flex gap-2'>
            <button className='btn' onClick={startAsUser}>Start as User</button>
            <button className='btn' onClick={startAsCompanion}>Start as Companion</button>
            <button className='btn' onClick={async ()=>{ await stop(); }}>End</button>
            <button className='btn' onClick={()=>toggleMic(false)}>Mute</button>
            <button className='btn' onClick={()=>toggleMic(true)}>Unmute</button>
          </div>
        </div>
        <div className='card'>
          <video ref={remoteRef} className='w-full h-64 bg-black rounded' autoPlay playsInline />
          <div className='mt-2'>
            <h4 className='font-medium'>Chat</h4>
            <div className='mt-2 h-40 overflow-auto bg-gray-50 p-2 rounded'>
              {messages.map((m,idx)=>(<div key={idx}><b>{m.from}:</b> {m.text}</div>))}
            </div>
            <div className='mt-2 flex gap-2'>
              <input value={chatText} onChange={e=>setChatText(e.target.value)} className='flex-1 p-2 border rounded' />
              <button className='btn' onClick={send}>Send</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
