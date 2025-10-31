interface Internship {
  id: string;
  title: string;
  company: string;
  location: string;
  description: string;
  requirements?: string;
  salary?: string;
  duration?: string;
  posted_date: string;
  source_url: string;
  source: string;
  remote?: boolean;
}

interface InternshipCardProps {
  internship: Internship;
}

export default function InternshipCard({ internship }: InternshipCardProps) {
  return (
    <div className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-200 p-6 border border-gray-200">
      <div className="flex justify-between items-start mb-3">
        <div className="flex-1">
          <h3 className="text-xl font-semibold text-gray-900 mb-1">
            {internship.title}
          </h3>
          <p className="text-lg text-blue-600 font-medium">
            {internship.company}
          </p>
        </div>
        {internship.remote && (
          <span className="bg-green-100 text-green-800 text-xs font-medium px-2.5 py-0.5 rounded-full">
            Remote
          </span>
        )}
      </div>
      
      <div className="mb-4">
        <p className="text-gray-600 mb-2">
          📍 {internship.location}
        </p>
        <p className="text-gray-700 text-sm leading-relaxed">
          {internship.description}
        </p>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4 text-sm">
        {internship.salary && (
          <div>
            <span className="font-medium text-gray-700">💰 Salary:</span>
            <span className="text-gray-600 ml-1">{internship.salary}</span>
          </div>
        )}
        {internship.duration && (
          <div>
            <span className="font-medium text-gray-700">⏱️ Duration:</span>
            <span className="text-gray-600 ml-1">{internship.duration}</span>
          </div>
        )}
        <div>
          <span className="font-medium text-gray-700">📅 Posted:</span>
          <span className="text-gray-600 ml-1">{internship.posted_date}</span>
        </div>
      </div>
      
      {internship.requirements && (
        <div className="mb-4">
          <h4 className="font-medium text-gray-700 mb-2">Requirements:</h4>
          <p className="text-gray-600 text-sm">{internship.requirements}</p>
        </div>
      )}
      
      <div className="flex justify-between items-center pt-4 border-t border-gray-200">
        <span className="text-xs text-gray-500">
          Source: {internship.source}
        </span>
        <a
          href={internship.source_url}
          target="_blank"
          rel="noopener noreferrer"
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors duration-200"
        >
          View Original Posting
        </a>
      </div>
    </div>
  );
}
