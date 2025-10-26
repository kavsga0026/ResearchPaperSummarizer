const SummaryCard = ({ title, summary }) => (
  <div className="bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-md p-5 mb-5 transition">
    <h3 className="text-blue-700 font-semibold text-lg mb-2 capitalize">{title}</h3>
    <p className="text-gray-700 leading-relaxed">{summary}</p>
  </div>
);

export default SummaryCard;
