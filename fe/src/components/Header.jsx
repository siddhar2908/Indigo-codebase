import { BarChart3, Compass, Folder, LogOut, Plane } from "lucide-react";

export default function Header() {
  return (
    <header className="header">
      <div className="brand">
        <Plane size={22} />
        <span>6E Creative Studio</span>
      </div>

      <nav className="nav">
        <button className="nav-item active">
          <Folder size={16} />
          Projects
        </button>

        <button className="nav-item">
          <Compass size={16} />
          Explore
        </button>

        <button className="nav-item">
          <BarChart3 size={16} />
          Analytics
        </button>
      </nav>

      <div className="user-area">
        <button className="signout">
          <LogOut size={16} />
          Sign out
        </button>
      </div>
    </header>
  );
}