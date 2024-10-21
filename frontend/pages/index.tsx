import React, { useState } from 'react';
import SearchForm from '../components/SearchForm';
import ResultList from '../components/ResultList';

const Home: React.FC = () => {
    type Result = {
      videoId: string;
      title: string; // タイトルを追加
      language: string; // 言語を追加
      viewCount: number; // 視聴回数を追加
      channelName: string; // チャンネル名を追加
      // 他のプロパティがあればここに追加
    };
    const [results, setResults] = useState<Result[]>([]);
    const [isLoading, setIsLoading] = useState(false); // 検索中の状態を追加
    const [isSummarizing, setIsSummarizing] = useState(false); // まとめ要約中の状態を追加

    const handleSearch = async (searchParams: { keyword: string, start: number, end: number }) => {
        console.log('searchParams : ' + searchParams.keyword + ' ' + searchParams.start + ' ' + searchParams.end);
        setIsLoading(true); // 検索開始時にisLoadingをtrueに設定
        try {
            //const response = await fetch('http://localhost:5001/api/search', {
            //const response = await fetch('/app2/api/search', {
                const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/search`, {// 環境変数からURLを取得
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(searchParams),
            });
            console.log('response : ' + response);
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            console.log('Search results:', data); // デバッグ用
            setResults(data);
        } catch (error) {
            console.error('Error fetching search results:', error);
        } finally {
            setIsLoading(false); // 検索終了時にisLoadingをfalseに設定
        }
    };

    const handleSummarize = async () => {
        //setIsLoading(true); // まとめ要約開始時にisLoadingをtrueに設定
        setIsSummarizing(true); // まとめ要約開始時にisSummarizingをtrueに設定

        try {
            //const response = await fetch('http://localhost:5001/api/summarize', {
            const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/summarize`, {// 環境変数からURLを取得
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ videoIds: results.map(result => result.videoId) }),
            });
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const summaryHtml = await response.text();
            const newWindow = window.open();
            if (newWindow) {
                newWindow.document.open(); // ドキュメントを開く
                newWindow.document.write(summaryHtml);
                newWindow.document.close(); // ドキュメントを閉じる
            }
        } catch (error) {
            console.error('Error summarizing results:', error);
        } finally {
            //setIsLoading(false); // まとめ要約終了時にisLoadingをfalseに設定
            setIsSummarizing(false); // まとめ要約終了時にisSummarizingをfalseに設定
        }
    };

    return (
        <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center">
            <h1 className="text-4xl font-bold mb-8">Youtube字幕検索</h1>
            <div className="w-full max-w-3xl"> {/* 検索ボックスとテロップのコンテナ */}
                {/* <SearchForm onSearch={handleSearch} /> */}
                <SearchForm onSearch={handleSearch} isLoading={isLoading} />
                {isSummarizing && (
                    <div className="bg-yellow-500 text-white text-center py-2 mt-4">
                        まとめ要約中！しばらくお待ちください！
                    </div>
                )}
            </div>
            {isLoading ? (
                <p>検索中...</p> // 検索中のメッセージを表示
            ) : results.length > 0 ? (
                <ResultList results={results} onSummarize={handleSummarize} />
            ) : (
                <p>検索結果がありません。</p>
            )}
        </div>
    );
};

export default Home;
