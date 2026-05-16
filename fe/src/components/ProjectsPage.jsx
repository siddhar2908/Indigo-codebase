import { Plus, Search } from "lucide-react";

export default function ProjectsPage({ onNewProject }) {
  return (
    <main className="page">
      <div className="page-header">
        <div>
          <h1>Projects</h1>
          <div className="stats">
            <span>0 Your Projects</span>
            <span>0 Creatives by You</span>
          </div>
        </div>

        <button className="primary-btn" onClick={onNewProject}>
          <Plus size={16} />
          New Project
        </button>
      </div>

      <div className="search-box">
        <Search size={18} />
        <input placeholder="Search projects..." />
      </div>

      <section className="project-grid single">
        <button className="new-project-card" onClick={onNewProject}>
          <div className="plus-circle">
            <Plus size={28} />
          </div>
          <span>New Project</span>
        </button>
      </section>
    </main>
  );
}