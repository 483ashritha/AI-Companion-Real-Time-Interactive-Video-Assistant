import { useEffect, useState } from 'react';
const BACKEND = process.env.NEXT_PUBLIC_BACKEND || 'http://localhost:8000';
export default function RecordingsPage(){
  const [list, setList] = useState([]);
  useEffect(()=>{ fetch(`${BACKEND}/api/recordings`).then(r=>r.json()).then(j=> setList(j.recordings || [])).catch(()=> setList([])); },[]);
  return (<div className='container'><h2 className='text-2xl font-semibold text-indigo-600'>Recordings</h2><div className='mt-4 grid gap-4'>{list.length===0 && <div className='card'>No recordings yet.</div>}{list.map((r:any)=>(<div key={r.recordingId} className='card'><p className='font-medium break-all'>{r.recordingId}</p><p className='text-sm text-gray-500'>Size: {r.size}</p><a className='btn mt-2' href={r.url} target='_blank'>Play</a></div>))}</div></div>);
}
