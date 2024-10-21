import React from 'react';

interface Result {
    title: string;
    videoId: string;
    language: string;
    viewCount: number;
    // 他のプロパティ
    channelName: string; // ここにchannelNameを追加
}

interface ResultListProps {
    results: Result[];
    onSummarize: () => void;
}

const ResultList: React.FC<ResultListProps> = ({ results, onSummarize }) => {
    console.log(results);
    console.log(results.length);
    return (
        <div className="w-full max-w-3xl mx-auto">
            {results.length > 0 && results.length <= 10 && (
                <div className="flex justify-end mb-4">
                    <button 
                        onClick={onSummarize} 
                        className="bg-green-500 text-white w-28 py-2 px-4 rounded hover:bg-green-600"
                    >
                        まとめ要約
                    </button>
                </div>
            )}
            <table className="w-full bg-white border-collapse">
                <thead>
                    <tr className="bg-gradient-to-r from-blue-500 to-purple-500 text-white">
                        <th className="py-2 pl-4 border-b border-r text-left">#</th>
                        <th className="py-2 border-b border-r">タイトル</th>
                        <th className="py-2 border-b border-r">言語</th>
                        <th className="py-2 border-b border-r">視聴回数</th>
                        <th className="py-2 border-b text-left min-w-[100px]">アクション</th>
                    </tr>
                </thead>
                <tbody>
                    {results.map((result, index) => (
                        <tr key={result.videoId} className={`border-t ${index % 2 === 0 ? 'bg-gray-100' : 'bg-white'}`}>
                            <td className="py-2 pl-4 border-r">{index + 1}</td>
                            <td className="py-2 pl-4 border-r">{result.title + " Channel : " + result.channelName}</td>
                            <td className="py-2 border-r">{result.language}</td>
                            <td className="py-2 border-r">{result.viewCount}</td>
                            <td className="py-2 text-center">
                                <a
                                    //href={`http://localhost:5001/api/download/${result.videoId}`}
                                    //href={`/app2/api/download/${result.videoId}`}
                                    href={`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/download/${result.videoId}`}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
                                >字幕要約</a>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default ResultList;
