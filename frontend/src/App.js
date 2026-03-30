import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [mode, setMode] = useState("detect");
  const [imageUrl, setImageUrl] = useState("");
  const [videoUrl, setVideoUrl] = useState("");
  const [labels, setLabels] = useState([]);
  const [annotations, setAnnotations] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleProcess = async () => {
    if (!file) {
      alert("Please upload a file first");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    setImageUrl("");
    setVideoUrl("");
    setLabels([]);
    setAnnotations([]);

    try {
      let response;

      if (mode === "detect") {
        response = await axios.post(
          "https://objectback-kyqp.vercel.app//detect",
          formData
        );
        setImageUrl(response.data.image_url);
        setLabels(response.data.labels);

      } else if (mode === "annotate") {
        response = await axios.post(
          "https://objectback-kyqp.vercel.app//annotations",
          formData
        );
        setAnnotations(response.data.annotations);

      } else if (mode === "cartoon") {
        response = await axios.post(
          "https://objectback-kyqp.vercel.app//cartoonize",
          formData
        );
        setImageUrl(response.data.image_url);

      } else if (mode === "video") {
        response = await axios.post(
          "https://objectback-kyqp.vercel.app//video-detect",
          formData
        );
        setVideoUrl(response.data.video_url);
      }

    } catch (error) {
      console.error(error);
      alert("Something went wrong");
    }

    setLoading(false);
  };

  return (
    <div className="app">
      <div className="background-overlay"></div>

      <header className="hero">
        <h1>AI Vision Suite</h1>
        <p>Smart Computer Vision for Images & Videos</p>
      </header>

      <div
        className="card"
        style={{
          maxWidth: "750px",
          margin: "auto",
          padding: "30px"
        }}
      >
        <select
          value={mode}
          onChange={(e) => setMode(e.target.value)}
          style={{
            padding: "12px",
            borderRadius: "10px",
            marginBottom: "20px",
            width: "100%"
          }}
        >
          <option value="detect">🎯 Object Detection</option>
          <option value="annotate">📝 Annotations</option>
          <option value="cartoon">🎨 Cartoonization</option>
          <option value="video">🎥 Video Detector</option>
        </select>

        <input
          type="file"
          onChange={(e) => setFile(e.target.files[0])}
          style={{
            marginBottom: "20px",
            width: "100%"
          }}
        />

        <button
          onClick={handleProcess}
          style={{
            width: "100%"
          }}
        >
          {loading ? "Processing..." : "Run Feature"}
        </button>

        {/* IMAGE OUTPUT */}
        {imageUrl && (
          <img
            src={imageUrl}
            alt="output"
            style={{
              width: "100%",
              marginTop: "25px",
              borderRadius: "16px"
            }}
          />
        )}

        {/* VIDEO DOWNLOAD OUTPUT */}
        {videoUrl && (
          <div
            style={{
              marginTop: "25px",
              padding: "20px",
              background: "#fff7ed",
              borderRadius: "16px",
              textAlign: "center"
            }}
          >
            <h3>🎥 Video Processed Successfully</h3>
            <p>Your detected video is ready for download.</p>

            <a
              href={videoUrl}
              download
              style={{
                display: "inline-block",
                marginTop: "15px",
                padding: "12px 24px",
                background: "#f59e0b",
                color: "white",
                textDecoration: "none",
                borderRadius: "10px",
                fontWeight: "bold"
              }}
            >
              ⬇️ Download Processed Video
            </a>
          </div>
        )}

        {/* LABELS */}
        {labels.length > 0 && (
          <div style={{ marginTop: "20px" }}>
            <h3>Detected Objects</h3>
            <ul>
              {labels.map((label, index) => (
                <li key={index}>{label}</li>
              ))}
            </ul>
          </div>
        )}

        {/* ANNOTATIONS */}
        {annotations.length > 0 && (
          <div style={{ marginTop: "20px" }}>
            <h3>Annotations</h3>
            {annotations.map((item, index) => (
              <div key={index}>
                <p><b>Label:</b> {item.label}</p>
                <p><b>Confidence:</b> {item.confidence}</p>
                <hr />
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;