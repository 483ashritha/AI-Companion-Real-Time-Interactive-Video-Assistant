import React, { useEffect, useState } from 'react';
import Link from 'next/link';
const BACKEND = process.env.NEXT_PUBLIC_BACKEND || 'http://localhost:8000';
export default function Companions(){
  const [companions, setCompanions] = useState<any[]>([]);
  useEffect(()=>{ fetch(`${BACKEND}/api/companions/`).then(r=>r.json()).then(d=>{ if(Array.isArray(d)) setCompanions(d); else if(d.data) setCompanions(d.data); else setCompanions(d); }).catch(()=> setCompanions([{id:'comp-1', name:'Ava', avatar:'https://i.pravatar.cc/150?img=1'},{id:'comp-2', name:'Kai', avatar:'https://i.pravatar.cc/150?img=2'}])); },[]);
  return (<div className='container'><h2 className='text-2xl font-semibold text-indigo-600'>Companions</h2><div className='grid gap-4 grid-cols-2 mt-4'>{companions.map((c:any)=>(<div key={c.id} className='card'><img src={c.avatar||c.image} alt='' className='w-20 h-20 rounded-full' /><h3 className='mt-2 font-medium'>{c.name}</h3><p className='text-sm text-gray-500'>Voice: {c.voiceId||'N/A'}</p><div className='mt-3'><Link href={{pathname:'/call/[roomId]', query:{roomId:'demo-'+c.id}}}><a className='btn'>Start Call</a></Link></div></div>))}</div></div>);
}
