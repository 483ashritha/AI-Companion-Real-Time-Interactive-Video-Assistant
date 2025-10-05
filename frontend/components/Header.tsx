import Link from 'next/link';
export default function Header(){
  return (
    <nav className="bg-white p-4 shadow-sm mb-4">
      <div className="container flex items-center gap-4">
        <Link href='/'><a className="font-semibold text-indigo-600">AI Companion</a></Link>
        <Link href='/companions'><a className="text-sm text-gray-700">Companions</a></Link>
        <Link href='/recordings'><a className="text-sm text-gray-700">Recordings</a></Link>
        <Link href='/settings'><a className="text-sm text-gray-700">Settings</a></Link>
        <Link href='/about'><a className="text-sm text-gray-700">About</a></Link>
      </div>
    </nav>
  );
}
