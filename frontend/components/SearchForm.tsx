import React, { useState } from 'react';

interface SearchFormProps {
    onSearch: (searchParams: { keyword: string, start: number, end: number, language: string }) => Promise<void>;
    isLoading: boolean;  // 検索中の状態を受け取る
}

const SearchForm: React.FC<SearchFormProps> = ({ onSearch, isLoading }) => {
    const [keyword, setKeyword] = useState('');
    const [start, setStart] = useState(1);
    const [end, setEnd] = useState(10);
    const [language, setLanguage] = useState('ja');

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        await onSearch({ keyword, start, end, language });
    };

    return (
        <div className="w-full max-w-3xl mx-auto mb-8">
            <form onSubmit={handleSubmit} className="bg-gradient-to-r from-blue-400 to-purple-500 p-6 shadow-lg rounded-lg">
                <div className="mb-6">
                    <label className="block text-white text-lg font-semibold mb-2" htmlFor="keyword">
                        キーワード
                    </label>
                    <input
                        id="keyword"
                        type="text"
                        value={keyword}
                        onChange={(e) => setKeyword(e.target.value)}
                        className="shadow appearance-none border border-gray-300 rounded w-full py-3 px-4 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-purple-600"
                        placeholder="検索キーワードを入力"
                    />
                </div>
                <div className="flex justify-between mb-6">
                    <div>
                        <label className="block text-white text-lg font-semibold mb-2" htmlFor="start">
                            開始
                        </label>
                        <input
                            id="start"
                            type="number"
                            value={start}
                            min={1}
                            onChange={(e) => setStart(Math.max(1, Number(e.target.value)))}
                            className="shadow appearance-none border border-gray-300 rounded w-20 py-3 px-4 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-purple-600"
                        />
                    </div>
                    <div>
                        <label className="block text-white text-lg font-semibold mb-2" htmlFor="end">
                            終了
                        </label>
                        <input
                            id="end"
                            type="number"
                            value={end}
                            onChange={(e) => setEnd(Number(e.target.value))}
                            className="shadow appearance-none border border-gray-300 rounded w-20 py-3 px-4 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-purple-600"
                        />
                    </div>
                    <div>
                        <label className="block text-white text-lg font-semibold mb-2" htmlFor="language">
                            言語
                        </label>
                        <select
                            id="language"
                            value={language}
                            onChange={(e) => setLanguage(e.target.value)}
                            className="shadow appearance-none border border-gray-300 rounded w-32 py-3 px-4 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-purple-600"
                        >
                            <option value="ja">日本語のみ</option>
                            <option value="ja+en">日本語含む</option>
                        </select>
                    </div>
                </div>
                <div className="flex justify-end">
                    <button
                        type="submit"
                        className="bg-yellow-500 hover:bg-yellow-600 text-white font-bold w-32 py-3 px-6 rounded-lg shadow-md focus:outline-none focus:ring-2 focus:ring-yellow-500"
                        disabled={isLoading}
                    >
                        {isLoading ? '検索中...' : '検索'}
                    </button>
                </div>
            </form>
        </div>
    );
};

export default SearchForm;
