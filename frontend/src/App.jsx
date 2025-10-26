import { useState } from "react";
import { FiUploadCloud } from "react-icons/fi";
import { motion } from "framer-motion";
import Loader from "./components/Loader";
import { summarizePDF, explainSection } from "./api";

function App() {
  const [file, setFile] = useState(null);
  const [fileName, setFileName] = useState("");
  const [summaries, setSummaries] = useState({});
  const [explanations, setExplanations] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [explaining, setExplaining] = useState(null);

  const handleFileUpload = (e) => {
    const selected = e.target.files[0];
    if (selected && selected.type === "application/pdf") {
      setFile(selected);
      setFileName(selected.name);
      setError("");
    } else {
      setError("Please upload a valid PDF file.");
    }
  };

  const handleSummarize = async () => {
    if (!file) {
      setError("Please upload a PDF first.");
      return;
    }
    setError("");
    setSummaries({});
    setExplanations({});
    setLoading(true);
    try {
      const res = await summarizePDF(file);
      setSummaries(res.summaries);
    } catch (err) {
      setError(err.response?.data?.detail || "Error while summarizing.");
    } finally {
      setLoading(false);
    }
  };

  const handleExplain = async (section, content) => {
    setExplaining(section);
    try {
      const res = await explainSection(content);
      setExplanations((prev) => ({ ...prev, [section]: res.explanation }));
    } catch (err) {
      setError("Error while explaining section.");
    } finally {
      setExplaining(null);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
      <div className="w-full max-w-3xl bg-white shadow-2xl rounded-3xl p-10 border border-gray-100">
        <motion.h1
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-4xl font-extrabold text-center text-blue-700 mb-4"
        >
          📘 Research Paper Summarizer
        </motion.h1>

        <p className="text-gray-600 text-center mb-8">
          Upload your research paper and get clear, section-wise summaries and simplified explanations.
        </p>

        {/* Upload Box */}
        <div className="border-2 border-dashed border-blue-400 rounded-xl p-6 flex flex-col items-center justify-center bg-blue-50 hover:bg-blue-100 transition">
          <input
            type="file"
            onChange={handleFileUpload}
            className="hidden"
            id="file-upload"
          />
          <label
            htmlFor="file-upload"
            className="cursor-pointer flex flex-col items-center text-blue-600"
          >
            <FiUploadCloud className="text-5xl mb-2" />
            <span className="font-medium">Upload your research paper (PDF)</span>
          </label>
          {fileName && <p className="text-gray-700 mt-3">{fileName}</p>}
        </div>

        {/* Error Message */}
        {error && (
          <p className="text-red-600 text-center mt-4 font-medium">{error}</p>
        )}

        {/* Summarize Button */}
        <button
          onClick={handleSummarize}
          disabled={loading}
          className={`mt-8 w-full ${
            loading ? "bg-gray-400" : "bg-blue-600 hover:bg-blue-700"
          } text-white py-3 rounded-lg text-lg font-semibold transition`}
        >
          {loading ? "Summarizing..." : "Summarize"}
        </button>

        {/* Loader */}
        {loading && <Loader />}

        {/* Summaries */}
        <div className="mt-10 space-y-6">
          {Object.entries(summaries).map(([section, content], idx) => (
            <motion.div
              key={idx}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4 }}
              className="p-6 bg-gray-50 rounded-lg shadow-md border hover:shadow-lg transition"
            >
              <h2 className="text-xl font-semibold text-blue-700 mb-2 capitalize">
                {section}
              </h2>
              <p className="text-gray-800 leading-relaxed">{content}</p>

              <button
                onClick={() => handleExplain(section, content)}
                disabled={explaining === section}
                className="mt-4 bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md text-sm font-medium"
              >
                {explaining === section ? "Explaining..." : "Explain Like I'm 10"}
              </button>

              {explanations[section] && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="mt-3 p-3 bg-indigo-50 rounded-lg border-l-4 border-indigo-400"
                >
                  <h3 className="text-indigo-700 font-semibold mb-1">
                    Simplified Explanation:
                  </h3>
                  <p className="text-gray-700">{explanations[section]}</p>
                </motion.div>
              )}
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default App;
