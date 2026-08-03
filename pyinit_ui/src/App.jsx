import { useState } from "react";

const API_BASE_URL = "http://127.0.0.1:8000";

function App() {
  const [projectName, setProjectName] = useState("my_app");
  const [stack, setStack] = useState("fastapi");
  const [pm, setPm] = useState("poetry");
  const [pythonVersion, setPythonVersion] = useState("3.12");
  const [docker, setDocker] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const isValidProjectName = (name) => /^[a-zA-Z][a-zA-Z0-9_-]*$/.test(name);

  const handleGenerate = async () => {
    setError("");
    setSuccess("");

    const trimmedName = projectName.trim();

    if (!trimmedName) {
      setError("Project name is required.");
      return;
    }

    if (!isValidProjectName(trimmedName)) {
      setError(
        "Project name must start with a letter and contain only letters, numbers, hyphen, or underscore."
      );
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/api/generate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: trimmedName,
          stack,
          pm,
          py: pythonVersion,
          ci: "github",
          docker,
        }),
      });

      if (!response.ok) {
     let message = "Unable to generate the project. Please try again.";

  try {
    const errorData = await response.json();

    if (typeof errorData.detail === "string") {
      message = errorData.detail;
    } else if (Array.isArray(errorData.detail)) {
      message = errorData.detail
        .map((item) => item.msg)
        .filter(Boolean)
        .join(", ");
    }
  } catch {
    // Keep the default message if the response is not JSON.
  }

  throw new Error(message);
}

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);

      const link = document.createElement("a");
      link.href = url;
      link.download = `${trimmedName}.zip`;
      document.body.appendChild(link);
      link.click();
      link.remove();

      window.URL.revokeObjectURL(url);
      setSuccess(`Project generated successfully. Downloading ${trimmedName}.zip...`);
    } catch (err) {
  if (err instanceof TypeError && err.message === "Failed to fetch") {
    setError(
      "Cannot connect to the PyInit backend. Please make sure the FastAPI server is running."
    );
  } else {
    setError(err.message || "Something went wrong.");
  }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.page}>
      <main style={styles.shell}>
        <section style={styles.hero}>
          <div style={styles.brandRow}>
            <div style={styles.logo}>🐍</div>
            <span style={styles.brand}>PyInit</span>
          </div>

          <h1 style={styles.title}>Start Python Projects Cleanly</h1>

          <p style={styles.subtitle}>
            Pick your stack, tooling, and defaults. PyInit generates a ready-to-use
            starter project as a ZIP.
          </p>

          <div style={styles.pills}>
            <span style={styles.pill}>FastAPI</span>
            <span style={styles.pill}>CLI</span>
            <span style={styles.pill}>Library</span>
            <span style={styles.pill}>Docker</span>
          </div>
        </section>

        <section style={styles.card}>
          <div style={styles.cardHeader}>
            <h2 style={styles.cardTitle}>Generate a project</h2>
            <p style={styles.cardSubtitle}>Configure your starter template.</p>
          </div>

          <div style={styles.form}>
            <div style={styles.field}>
              <label style={styles.label}>Project name</label>
              <input
                type="text"
                value={projectName}
                onChange={(e) => setProjectName(e.target.value)}
                placeholder="inventory_api"
                style={styles.input}
              />
              <span style={styles.helpText}>
                Use letters, numbers, hyphen, or underscore.
              </span>
            </div>

            <div style={styles.grid}>
              <div style={styles.field}>
                <label style={styles.label}>Stack</label>
                <select
                  value={stack}
                  onChange={(e) => setStack(e.target.value)}
                  style={styles.input}
                >
                  <option value="fastapi">FastAPI API</option>
                  <option value="lib">Python Library</option>
                  <option value="cli">CLI Tool</option>
                </select>
              </div>

              <div style={styles.field}>
                <label style={styles.label}>Package manager</label>
                <select
                  value={pm}
                  onChange={(e) => setPm(e.target.value)}
                  style={styles.input}
                >
                  <option value="poetry">Poetry</option>
                  <option value="hatch">Hatch</option>
                  <option value="pdm">PDM</option>
                </select>
              </div>
            </div>

            <div style={styles.grid}>
              <div style={styles.field}>
                <label style={styles.label}>Python version</label>
                <select
                  value={pythonVersion}
                  onChange={(e) => setPythonVersion(e.target.value)}
                  style={styles.input}
                >
                  <option value="3.12">Python 3.12</option>
                  <option value="3.11">Python 3.11</option>
                  <option value="3.10">Python 3.10</option>
                  <option value="3.9">Python 3.9</option>
                </select>
              </div>

              <div style={styles.field}>
                <label style={styles.label}>Options</label>
                <label style={styles.checkboxBox}>
                  <input
                    type="checkbox"
                    checked={docker}
                    onChange={(e) => setDocker(e.target.checked)}
                    style={styles.checkbox}
                  />
                  <span>
                    <strong>Dockerfile</strong>
                    <small style={styles.checkboxText}>Include container support</small>
                  </span>
                </label>
              </div>
            </div>

            <button
              onClick={handleGenerate}
              disabled={loading}
              style={loading ? styles.buttonDisabled : styles.button}
            >
              {loading ? "Generating project..." : "Generate ZIP"}
            </button>

            {success && <div style={styles.success}>{success}</div>}
            {error && <div style={styles.error}>{error}</div>}
          </div>
        </section>

        <footer style={styles.footer}>
          Built with React + FastAPI · Powered by your PyInit generator engine
        </footer>
      </main>
    </div>
  );
}

const styles = {
  page: {
    minHeight: "100vh",
    background:
      "radial-gradient(circle at top left, #dbeafe 0, transparent 32%), radial-gradient(circle at bottom right, #ccfbf1 0, transparent 28%), #f8fafc",
    display: "flex",
    justifyContent: "center",
    padding: "42px 20px",
    fontFamily:
      "Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    color: "#0f172a",
  },
  shell: {
    width: "100%",
    maxWidth: "900px",
  },
  hero: {
    textAlign: "center",
    marginBottom: "22px",
  },
  brandRow: {
    display: "inline-flex",
    alignItems: "center",
    gap: "10px",
    padding: "8px 14px",
    borderRadius: "999px",
    background: "#ffffff",
    border: "1px solid #e2e8f0",
    boxShadow: "0 8px 24px rgba(15, 23, 42, 0.06)",
    marginBottom: "18px",
  },
  logo: {
    width: "28px",
    height: "28px",
    display: "grid",
    placeItems: "center",
    borderRadius: "8px",
    background: "#eef2ff",
    fontSize: "17px",
  },
  brand: {
    fontSize: "15px",
    fontWeight: 800,
    color: "#4338ca",
  },
  title: {
    margin: 0,
    fontSize: "42px",
    lineHeight: 1.05,
    letterSpacing: "-0.055em",
    fontWeight: 900,
    color: "#0f172a",
  },
  subtitle: {
    maxWidth: "680px",
    margin: "14px auto 0",
    color: "#64748b",
    fontSize: "17px",
    lineHeight: 1.65,
  },
  pills: {
    display: "flex",
    justifyContent: "center",
    flexWrap: "wrap",
    gap: "10px",
    marginTop: "18px",
  },
  pill: {
    padding: "7px 12px",
    borderRadius: "999px",
    background: "#eef2ff",
    color: "#3730a3",
    fontSize: "13px",
    fontWeight: 700,
  },
  card: {
    background: "rgba(255, 255, 255, 0.92)",
    border: "1px solid #e2e8f0",
    borderRadius: "24px",
    padding: "30px",
    boxShadow: "0 30px 90px rgba(15, 23, 42, 0.13)",
    backdropFilter: "blur(10px)",
  },
  cardHeader: {
    marginBottom: "22px",
  },
  cardTitle: {
    margin: 0,
    fontSize: "22px",
    fontWeight: 850,
    letterSpacing: "-0.025em",
  },
  cardSubtitle: {
    margin: "6px 0 0",
    color: "#64748b",
    fontSize: "14px",
  },
  form: {
    display: "flex",
    flexDirection: "column",
    gap: "18px",
  },
  grid: {
    display: "grid",
    gridTemplateColumns: "1fr 1fr",
    gap: "18px",
  },
  field: {
    display: "flex",
    flexDirection: "column",
    gap: "8px",
  },
  label: {
    fontSize: "13px",
    fontWeight: 800,
    color: "#334155",
    textAlign: "left",
  },
  input: {
    width: "100%",
    boxSizing: "border-box",
    height: "50px",
    padding: "0 14px",
    borderRadius: "14px",
    border: "1px solid #cbd5e1",
    fontSize: "15px",
    outline: "none",
    background: "#ffffff",
    color: "#0f172a",
  },
  helpText: {
    color: "#64748b",
    fontSize: "12px",
  },
  checkboxBox: {
    height: "50px",
    boxSizing: "border-box",
    display: "flex",
    alignItems: "center",
    gap: "12px",
    padding: "0 14px",
    borderRadius: "14px",
    border: "1px solid #cbd5e1",
    background: "#ffffff",
    cursor: "pointer",
  },
  checkbox: {
    width: "18px",
    height: "18px",
  },
  checkboxText: {
    display: "block",
    marginTop: "2px",
    color: "#64748b",
    fontSize: "12px",
    fontWeight: 500,
  },
  button: {
    marginTop: "4px",
    width: "100%",
    height: "54px",
    border: "none",
    borderRadius: "16px",
    background: "linear-gradient(135deg, #4f46e5, #2563eb)",
    color: "#ffffff",
    fontSize: "16px",
    fontWeight: 850,
    cursor: "pointer",
    boxShadow: "0 14px 30px rgba(79, 70, 229, 0.28)",
  },
  buttonDisabled: {
    marginTop: "4px",
    width: "100%",
    height: "54px",
    border: "none",
    borderRadius: "16px",
    background: "#94a3b8",
    color: "#ffffff",
    fontSize: "16px",
    fontWeight: 850,
    cursor: "not-allowed",
  },
  success: {
    padding: "14px 16px",
    borderRadius: "14px",
    background: "#ecfdf5",
    color: "#047857",
    fontSize: "14px",
    fontWeight: 800,
  },
  error: {
    padding: "14px 16px",
    borderRadius: "14px",
    background: "#fef2f2",
    color: "#b91c1c",
    fontSize: "14px",
    fontWeight: 800,
  },
  footer: {
    textAlign: "center",
    color: "#64748b",
    fontSize: "13px",
    marginTop: "18px",
  },
};

export default App;