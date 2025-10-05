import { useRef, useState } from 'react';
import { io, Socket } from 'socket.io-client';

export function useWebRTC(backendUrl: string){
  const pcRef = useRef<RTCPeerConnection|null>(null);
  const localStreamRef = useRef<MediaStream|null>(null);
  const [localStream, setLocalStream] = useState<MediaStream|null>(null);
  const [remoteStream, setRemoteStream] = useState<MediaStream|null>(null);
  const socketRef = useRef<Socket|null>(null);
  let currentRoom = '';

  async function startLocal(constraints: MediaStreamConstraints = { audio: true, video: true }){
    const stream = await navigator.mediaDevices.getUserMedia(constraints);
    localStreamRef.current = stream;
    setLocalStream(stream);
    return stream;
  }

  async function createPC(iceServers: any = [{ urls: 'stun:stun.l.google.com:19302' }]){
    const pc = new RTCPeerConnection({ iceServers });
    pc.onicecandidate = (e) => {
      if (e.candidate && socketRef.current){
        const payload = (e.candidate as any)?.toJSON ? (e.candidate as any).toJSON() : e.candidate;
        socketRef.current.emit('candidate', { candidate: payload, roomId: currentRoom });
      }
    };
    pc.ontrack = (e) => setRemoteStream(e.streams[0]);
    if (localStreamRef.current) localStreamRef.current.getTracks().forEach(t => pc.addTrack(t, localStreamRef.current as MediaStream));
    pcRef.current = pc;
    return pc;
  }

  function connectSocket(roomId: string, userId: string, onEvent?: (ev:string,payload:any)=>void){
    currentRoom = roomId;
    const socket = io( (backendUrl || '') , { path: '/socket.io', transports: ['websocket'] });
    socketRef.current = socket;
    socket.on('connect', ()=> socket.emit('join', { roomId, userId }));
    socket.on('offer', async (data:any)=> {
      if (!pcRef.current){
        const cfg = await fetch(`${backendUrl}/api/webrtc/config`).then(r=>r.json());
        await createPC(cfg.iceServers);
      }
      await pcRef.current!.setRemoteDescription(new RTCSessionDescription(data.sdp));
      const answer = await pcRef.current!.createAnswer();
      await pcRef.current!.setLocalDescription(answer);
      socket.emit('answer', { sdp: pcRef.current!.localDescription, roomId });
    });
    socket.on('answer', async (data:any)=> { if (pcRef.current && data.sdp) await pcRef.current.setRemoteDescription(new RTCSessionDescription(data.sdp)); });
    socket.on('candidate', async (data:any)=> { try { if (pcRef.current && data.candidate) await pcRef.current.addIceCandidate(new RTCIceCandidate(data.candidate)); } catch(e){ console.warn('candidate err', e); } });
    socket.on('chat', (d:any)=> onEvent && onEvent('chat', d));
    socket.on('join', (d:any)=> onEvent && onEvent('join', d));
    socket.on('leave', (d:any)=> onEvent && onEvent('leave', d));
    return socket;
  }

  async function createOffer(roomId: string){
    const cfg = await fetch(`${backendUrl}/api/webrtc/config`).then(r=>r.json()).catch(()=>({iceServers:[{urls:['stun:stun.l.google.com:19302']}] }));
    if (!pcRef.current) await createPC(cfg.iceServers);
    const offer = await pcRef.current!.createOffer();
    await pcRef.current!.setLocalDescription(offer);
    socketRef.current?.emit('offer', { sdp: pcRef.current!.localDescription, roomId });
  }

  function sendChat(text: string){ socketRef.current?.emit('chat', { roomId: currentRoom, text, from: 'user' }); }
  async function stop(){ pcRef.current?.close(); pcRef.current = null; localStreamRef.current?.getTracks().forEach(t => t.stop()); localStreamRef.current = null; setLocalStream(null); setRemoteStream(null); socketRef.current?.disconnect(); socketRef.current = null; }
  function toggleMic(enabled:boolean){ localStreamRef.current?.getAudioTracks().forEach(t=>t.enabled = enabled); }
  function toggleCam(enabled:boolean){ localStreamRef.current?.getVideoTracks().forEach(t=>t.enabled = enabled); }
  return { startLocal, createPC, connectSocket, createOffer, sendChat, stop, localStream, remoteStream, toggleMic, toggleCam };
}
