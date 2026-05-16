import { useState } from "react";
import Header from "./components/Header";
import ProjectsPage from "./components/ProjectsPage";
import ProjectCreatePage from "./components/ProjectCreatePage";

export default function App() {
  const [page, setPage] = useState("projects");

  return (
    <div className="app">
      <Header />

      {page === "projects" && (
        <ProjectsPage onNewProject={() => setPage("create")} />
      )}

      {page === "create" && (
        <ProjectCreatePage
          projectName="New Project"
          onBack={() => setPage("projects")}
        />
      )}
    </div>
  );
}