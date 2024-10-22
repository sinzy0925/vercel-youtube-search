from flask import Flask, request, jsonify, make_response, send_file
from flask_cors import CORS
from youtubesearchpython import VideosSearch
from langdetect import detect
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
import os
import google.generativeai as genai
import markdown
import requests
import traceback
import subprocess
import glob
import tempfile
import yt_dlp
import shutil
import time
from dotenv import load_dotenv
#
#

# .envファイルを読み込む
load_dotenv()

# 環境変数からプロキシとAPIキーを取得
proxy_server = os.getenv('PROXY_SERVER')
api_key = os.getenv('API_KEY')


app = Flask(__name__)
CORS(app)  # すべてのオリジンを許可

youyaku_shijibun = """
日本語で解答してください。
ソースコードは不要です。
以下の#内容:をもとにビジネス活用例を詳細に教えてください。
出力は以下の順でお願いします。
1.概要2.ビジネス活用事例詳細3.メリット4.デメリット5.できる事まとめ
#内容:
"""

langlist = ['ja','en','aa', 'af', 'ak', 'sq', 'am', 'ar', 'hy', 'as', 'ay', 'az', 'bn', 'ba', 'eu', 'be', 'bho', 'bs', 'br', 'bg', 'my', 'ca', 'ceb', 'zh-Hans', 'zh-Hant', 'co', 'hr', 'cs', 'da', 'dv', 'nl', 'dz','eo', 'et', 'ee', 'fo', 'fj', 'fil', 'fi', 'fr', 'gaa', 'gl', 'lg', 'ka', 'de', 'el', 'gn', 'gu', 'ht', 'ha', 'haw', 'iw', 'hi', 'hmn', 'hu', 'is', 'ig', 'id', 'ga', 'it', 'jv', 'kl', 'kn', 'kk', 'kha', 'km', 'rw', 'ko', 'kri', 'ku', 'ky', 'lo', 'la', 'lv', 'ln', 'lt', 'luo', 'lb', 'mk', 'mg', 'ms', 'ml', 'mt', 'gv', 'mi', 'mr', 'mn', 'mfe', 'ne', 'new', 'nso', 'no', 'ny', 'oc', 'or', 'om', 'os', 'pam', 'ps', 'fa', 'pl', 'pt', 'pt-PT', 'pa', 'qu', 'ro', 'rn', 'ru', 'sm', 'sg', 'sa', 'gd', 'sr', 'crs', 'sn', 'sd', 'si', 'sk', 'sl', 'so', 'st', 'es', 'su', 'sw', 'ss', 'sv', 'tg', 'ta', 'tt', 'te', 'th', 'bo', 'ti', 'to', 'ts', 'tn', 'tum', 'tr', 'tk', 'uk', 'ur', 'ug', 'uz', 've', 'vi', 'war', 'cy', 'fy', 'wo', 'xh', 'yi', 'yo', 'zu']
language_codes = [
    'ja',  # 日本語
    'en',  # 英語
    'zh',  # 中国語
]
language_codes2 = [
    'hi',  # ヒンディー語
    'es',  # スペイン語
    'fr',  # フランス語
    'ar',  # アラビア語
    'bn',  # ベンガル語
    'pt',  # ポルトガル語
    'ru',  # ロシア語
    'de',  # ドイツ語
    'ko',  # 韓国語
    'it',  # イタリア語
    'tr',  # トルコ語
    'vi',  # ベトナム語
    'pl',  # ポーランド語
    'uk',  # ウクライナ語
    'fa',  # ペルシャ語
    'th',  # タイ語
    'sw',  # スワヒリ語
    'nl',  # オランダ語
    'ro',  # ルーマニア語
    'hu',  # ハンガリー語
    'cs',  # チェコ語
    'el',  # ギリシャ語
    'da',  # デンマーク語
    'fi',  # フィンランド語
    'he',  # ヘブライ語
    'no',  # ノルウェー語
    'sk',  # スロバキア語
    'sl',  # スロベニア語
]

@app.route("/")
def hello_world():
   return "<p>path : /  hello world</p>"

@app.route("/api/test")
def test():
   return "<p>path : /api/test  hello world</p>"

@app.route('/api/search', methods=['POST'])
def search():
    def get_many_videos(search_query, limit):
        videos_search = VideosSearch(search_query, limit=limit)
        results = []
        
        while len(results) < limit:
            batch = videos_search.result()["result"]
            for video in batch:
                # チャンネルIDがNoneでないことを確認
                if video['channel']['id'] is not None:
                    results.append(video)
                    #print(video)
                    #print(f"channel_id: {video['channel']['id']}")
            
            if not videos_search.next():
                break  
        
        return results[:limit]
    
    def is_recent_video(published_time):
        return "year" not in published_time and "years" not in published_time
  
    data = request.json
    keyword = data['keyword']
    start = data['start']
    end = data['end']
    language_filter = data['language']

    search = get_many_videos(keyword, limit=end+30)
    results = search
    print(f"Total results fetched: {len(results)}")


    sorted_results = sorted(results, key=lambda x: int(x['viewCount']['text'].split()[0].replace(',', '')), reverse=True)

    
    filtered_results = [
        video for video in sorted_results 
        if is_recent_video(video['publishedTime']) 
    ]

    filtered = []

    for result in filtered_results[start-1:end]:
        title = result['title']
        video_id = result['id']
        published_time = result['publishedTime']
        view_count = result['viewCount']['text'].split()[0]
        channel_name = result['channel']['name']
        if 'descriptionSnippet' in result:
            descriptionSnippet = result['descriptionSnippet']
            #print("descriptionSnippet: ")
            #print(descriptionSnippet)

        else:
            descriptionSnippet = ""

        language = detect(title)

        if language_filter == 'ja' and language == 'ja':
        #if language == 'ja':
            filtered.append({
                'title': title,
                'videoId': video_id,
                'publishedTime': published_time,
                'viewCount': view_count,
                'descriptionSnippet': descriptionSnippet,
                'channelName': channel_name,
                'language': 'ja'
            })
        elif language_filter == 'ja+en' and language in language_codes:
            filtered.append({
                'title': title,
                'videoId': video_id,
                'publishedTime': published_time,
                'viewCount': view_count,
                'descriptionSnippet': descriptionSnippet,
                'channelName': channel_name,
                'language': language
            })

    response = make_response(jsonify(filtered))
    #response.headers['Access-Control-Allow-Origin'] = 'https://frontend-82bjg1bhp-taros-projects-ed87193f.vercel.app'
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
#




@app.route('/api/download/<video_id>', methods=['GET'])
def download(video_id):
    # 処理の開始時刻を記録
    start_time = time.time()    
    print('download video_id', video_id)
    try:
        # APIキーの設定
        genai.configure(api_key=api_key)

        print('try download video_id', video_id)

        print('try download_subtitles', video_id)

        video_url = f'https://www.youtube.com/watch?v={video_id}'
        #transcript_text = download_subtitles(video_url)


        transcript = YouTubeTranscriptApi.get_transcript(
            video_id, 
            languages = langlist, 
            proxies={"https": proxy_server}
            )
        
        transcript_text = ""
        for entry in transcript:
            transcript_text += (f"{entry['text']}")

        print(f"download transcript  time: {time.time() - start_time} sec")


        # Geminiモデルの設定
        model = genai.GenerativeModel('gemini-1.5-flash')
        # 字幕テキストを要約する
        response = model.generate_content(
            f"{youyaku_shijibun}{transcript_text}",
            generation_config = genai.GenerationConfig(
                max_output_tokens=3000,
                temperature=0.1,
            )
        )
        summary_markdown = response.text
        summary_html = markdown.markdown(summary_markdown)

        url =  f'https://www.youtube.com/watch?v={video_id}'
        url_html = f'<a href="{url}" target="_blank">{url}</a><br>'
        summary_html = url_html + summary_html

        print(f"download LLM summary time: {time.time() - start_time} sec")

        return summary_html

        #file_path = f"{video_id}.html"
        #with open(file_path, 'w', encoding='utf-8') as f:
        #   for entry in transcript:
        #       f.write(f"{entry['text']}")
        #       f.write(f"{summary_html}")

        #if not os.path.exists(file_path):
        #    return jsonify({'error': 'File not found'}), 404

        #return send_file(file_path, as_attachment=True)
        # ダウンロード時のファイル名を指定
        #return send_file(file_path, as_attachment=True, download_name=f"{video_id}.html")
        # as_attachment=Falseを指定して、ブラウザで直接表示
        #return send_file(file_path, as_attachment=False)

    except TranscriptsDisabled:
        print(f"download 字幕が無効なため、動画 {video_id} のトランスクリプトを取得できません。")
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

def process_video(video_id):
    print('process_video', video_id)
    try:
        # APIキーの設定
        genai.configure(api_key=api_key)

        print('try process_video', video_id)

        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        for transcript in transcript_list:
            print(transcript.language)


        transcript = YouTubeTranscriptApi.get_transcript(
            video_id, 
            languages = langlist, 
            proxies={"https": proxy_server}
            )
        
        transcript_text = ""
        for entry in transcript:
            transcript_text += (f"{entry['text']}")
        
        # Geminiモデルの設定
        model = genai.GenerativeModel('gemini-1.5-flash')
        # 字幕テキストを要約する
        response = model.generate_content(
            f"{youyaku_shijibun}{transcript_text}",
            generation_config = genai.GenerationConfig(
                max_output_tokens=3000,
                temperature=0.1,
            )
        )
        summary_markdown = response.text
        summary_html = markdown.markdown(summary_markdown)

        url =  f'https://www.youtube.com/watch?v={video_id}'
        url_html = f'<a href="{url}" target="_blank">{url}</a><br>'
        summary_html = url_html + summary_html 

        return summary_html

    except TranscriptsDisabled:
        print(f"process_video 字幕が無効なため、動画 {video_id} のトランスクリプトを取得できません。")

    except Exception as e:
        traceback.print_exc()
        return f"<p>Error processing video {video_id}: {str(e)}</p>"

@app.route('/api/summarize', methods=['POST'])
def summarize():
    data = request.json
    print(data)
    video_ids = data.get('videoIds', [])
    summaries = []

    for index, video_id in enumerate(video_ids):
        summary_html = process_video(video_id)
        summaries.append("<h3>"+str(index + 1) + ".</h3>" + summary_html+ "<hr>")
        print(video_id)

    # HTMLを生成する処理
    summary_html = "<html><body>" + "".join(summaries) + "</body></html>"
    return summary_html

#if __name__ == '__main__':
    #app.run(debug=True)#, host='0.0.0.0', port=5000)  # ホストとポートを指定
    #app.run(debug=True, host='0.0.0.0', port=5000)  # ホストとポートを指定
    #CORS(app)  # これにより、すべてのオリジンからのリクエストを許可します
    #app.run(debug=True)

# 以下使ってない
# 字幕のダウンロード
def download_subtitles(video_url):
    # 既存の.vttファイルを削除
    #clear_vtt_files('api')
    with tempfile.TemporaryDirectory() as tmpdirname:
        # 一時ディレクトリにクッキーファイルをコピー
        temp_cookie_path = os.path.join(tmpdirname, 'cookies.txt')
        shutil.copy('./api/youtube_cookies.txt', temp_cookie_path)
        print("try temp_cookie_path : ", temp_cookie_path)


        output_path = os.path.join(tmpdirname, 'output.vtt')
        print("try output_path : ", output_path)
        # yt-dlpコマンドでoutput_pathを使用
        # yt-dlpコマンドを構築
        command = [
            #'./api/yt-dlp',
            'yt-dlp',
            '--cookies', temp_cookie_path,
            '--user-agent', "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
            '--write-auto-sub',
            '--sub-lang', 'ja',
            '--skip-download',
            '--sub-format', 'vtt',
            '-o', output_path,
            #'-o', os.path.join('api', 'bbb.%(ext)s'),
            #'-o', '-',  # 標準出力に出力
            video_url
        ]
        print("try command : ", command)
        try:


            # コマンドを実行
            #result = subprocess.run(command, check=True)
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            print("try yt-dlp output:", result.stdout)
            print("try yt-dlp errors:", result.stderr)
            
            print("try 字幕のダウンロードが完了しました。")
            # ファイルを読み取る
            subtitles = []
            with open(output_path + '.ja.vtt', 'r', encoding='utf-8') as file:
                #content = file.read()
                #print("ファイルの内容:")
                #print(content)
                lines = file.readlines()
        
                line_previous = None
                for line in lines:
                    # タイムスタンプや空行をスキップ
                    if '<' in line or line.strip() == '':
                        continue
                    if '-->' in line or line.strip() == '':
                        continue
                    # 字幕テキストを追加
                    if line != line_previous:
                        subtitles.append(line.strip())
                        line_previous = line
            text = ""
            for subtitle in subtitles:
                text += subtitle
            
            print(text)
 
            return text

        
        except subprocess.CalledProcessError as e:
            traceback.print_exc()
            print("try Command output:", e.output)
            print("try Command stderr:", e.stderr)
            print(f"try errエラーが発生しました: {e}")


#yt-dlp --write-auto-sub --sub-lang ja --skip-download --sub-format vtt -o aaa https://www.youtube.com/watch?v=OagYLOhxf6A
#/api/download/p56_8JTvu8M
