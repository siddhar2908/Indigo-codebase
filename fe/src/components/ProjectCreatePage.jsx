import { useState } from "react";
import {
  ChevronLeft,
  FileText,
  Image,
  LayoutTemplate,
  Share2
} from "lucide-react";

const API_BASE_URL = "http://localhost:5000";

export default function ProjectCreatePage({ projectName, onBack }) {
  const [activeTab, setActiveTab] = useState("Social");
  const [campaignType, setCampaignType] = useState("");
  const [platform, setPlatform] = useState("");
  const [campaignDescription, setCampaignDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [textResult, setTextResult] = useState("");
  const [imageResult, setImageResult] = useState("");
  const [imageError, setImageError] = useState("");

  const handleGenerate = async () => {
    setTextResult("");
    setImageResult("");
    setImageError("");

    if (!campaignType || !campaignDescription) {
      alert("Please fill Campaign Type and Campaign Description.");
      return;
    }

    if (activeTab === "Social" && !platform) {
      alert("Please select a platform.");
      return;
    }

    let endpoint = "";

    if (activeTab === "Social") {
      endpoint = "/api/generate/social";
    } else if (activeTab === "Copywriting") {
      endpoint = "/api/generate/copywriting";
    } else if (activeTab === "Banner") {
      endpoint = "/api/generate/banner";
    }

    try {
      setLoading(true);

      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          campaignType,
          campaignDescription,
          platform
        })
      });

      const data = await response.json();

      if (!response.ok) {
        alert(data.error || "Something went wrong");
        return;
      }

      if (data.result) {
        setTextResult(data.result);
      }

      if (data.imageBase64 && data.mimeType) {
        setImageResult(`data:${data.mimeType};base64,${data.imageBase64}`);
      }

      if (data.imageError) {
        setImageError(JSON.stringify(data.imageError, null, 2));
      }

      if (!data.result && !data.imageBase64 && !data.imageError) {
        alert("No output returned from backend.");
      }
    } catch (error) {
      console.error(error);
      alert("Backend connection failed. Please make sure Flask is running.");
    } finally {
      setLoading(false);
    }
  };

  const handleTabChange = (tabName) => {
    setActiveTab(tabName);
    setTextResult("");
    setImageResult("");
    setImageError("");

    if (tabName !== "Social") {
      setPlatform("");
    }
  };

  return (
    <main className="project-create">
      <div className="breadcrumb">
        <button onClick={onBack}>
          <ChevronLeft size={18} />
          Projects
        </button>
        <span>/</span>
        <strong>{projectName}</strong>
      </div>

      <div className="tool-tabs">
        {[
          { name: "Social", icon: Share2 },
          { name: "Copywriting", icon: FileText },
          { name: "Banner", icon: Image }
        ].map((tab) => {
          const Icon = tab.icon;

          return (
            <button
              key={tab.name}
              className={`tool-tab ${activeTab === tab.name ? "active" : ""}`}
              onClick={() => handleTabChange(tab.name)}
            >
              <Icon size={16} />
              {tab.name}
            </button>
          );
        })}
      </div>

      <div className="create-layout">
        <aside className="details-card">
          <h2>Campaign Details</h2>

          <label>
            Campaign Type <span>*</span>
          </label>

          <select
            value={campaignType}
            onChange={(event) => setCampaignType(event.target.value)}
          >
            <option value="">Select campaign type...</option>
            <option value="Offer">Offer</option>
            <option value="Sales">Sales</option>
            <option value="Route Launch">Route Launch</option>
            <option value="Festival Campaign">Festival Campaign</option>
          </select>

          {activeTab === "Social" && (
            <>
              <label>
                Platform <span>*</span>
              </label>

              <select
                value={platform}
                onChange={(event) => setPlatform(event.target.value)}
              >
                <option value="">Select platform...</option>
                <option value="Instagram Post">Instagram Post</option>
                <option value="Facebook Post">Facebook Post</option>
                <option value="Linkedin Post">Linkedin Post</option>
                <option value="X.com Post">X.com Post</option>
                <option value="Instagram Reel Caption">
                  Instagram Reel Caption
                </option>
              </select>
            </>
          )}

          <label>
            Describe your campaign <span>*</span>
          </label>

          <textarea
            value={campaignDescription}
            onChange={(event) => setCampaignDescription(event.target.value)}
            placeholder="e.g. Show a cricket batter hitting a shot with an IndiGo plane flying safely above the stadium. Promote 25% off flight tickets for 1 month."
          />

          <button
            className="generate-btn"
            onClick={handleGenerate}
            disabled={loading}
          >
            {loading ? "Generating..." : `Generate ${activeTab}`}
          </button>
        </aside>

        <section className="generation-area">
          {!textResult && !imageResult && !imageError && (
            <div className="empty-state">
              <div className="empty-icon">
                <LayoutTemplate size={32} />
              </div>

              <h2>Ready to create your {activeTab.toLowerCase()} campaign?</h2>

              <p>
                Fill out the campaign details on the left to generate tailored
                content for your {activeTab.toLowerCase()} creatives.
              </p>
            </div>
          )}

          {(textResult || imageResult || imageError) && (
            <div className="result-box">
              <h2>{activeTab} Output</h2>

              {textResult && <pre>{textResult}</pre>}

              {imageResult && (
                <div className="generated-image-wrap">
                  <h3>Generated Image</h3>
                  <img
                    src={imageResult}
                    alt={`${activeTab} generated creative`}
                  />
                </div>
              )}

              {imageError && (
                <div className="error-box">
                  <h3>Image generation failed</h3>
                  <pre>{imageError}</pre>
                </div>
              )}
            </div>
          )}
        </section>
      </div>
    </main>
  );
}