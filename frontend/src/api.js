import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL;

// 🧩 1️⃣ Function for summarization
export const summarizePDF = async (file) => {
  const formData = new FormData();
  formData.append("pdf", file);
  const res = await axios.post(`${API_URL}/summarize`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return res.data;
};

// 🧩 2️⃣ Function for explanation (Explain Like I'm 10)
export const explainSection = async (summaryText) => {
  const res = await axios.post(`${API_URL}/explain`, { summary: summaryText });
  return res.data;
};
