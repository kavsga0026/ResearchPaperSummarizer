import { useState } from "react";
import { FiUploadCloud } from "react-icons/fi";

const FileUploader = ({ onSelect }) => {
  const [fileName, setFileName] = useState("");

  const handleFile = (e) => {
    const file = e.target.files[0];
    if (file && file.type === "application/pdf") {
      setFileName(file.name);
      onSelect(file);
    } else {
      alert("Please upload a valid PDF file!");
    }
  };

  return (
    <div className="border-2 border-dashed border-blue-400 bg-white rounded-xl shadow-sm hover:shadow-md p-8 text-center transition-all">
      <FiUploadCloud className="text-blue-600 text-4xl mx-auto mb-2" />
      <p className="text-gray-600 mb-2">Upload your research paper (PDF)</p>
      <input type="file" accept="application/pdf" onChange={handleFile} className="cursor-pointer" />
      {fileName && <p className="text-sm text-gray-500 mt-3">{fileName}</p>}
    </div>
  );
};

export default FileUploader;
