import os

def create_directory_structure(directory_structure: list):
  """
  配列からディレクトリ構造を作成する関数。

  Args:
    directory_structure: ディレクトリ構造を表す配列。
  """

  def create_directory_recursive(path: str, structure: list):
    """
    再帰的にディレクトリを作成する関数。

    Args:
      path: 作成するディレクトリのパス。
      structure: ディレクトリ構造を表す配列。
    """
    for item in structure:
      if isinstance(item, str):
        # ファイルの作成
        file_path = os.path.join(path, item)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
          pass  # ファイルに空のコンテンツを書き込む
      elif isinstance(item, list):
        # フォルダの作成
        dir_path = os.path.join(path, item[0])
        os.makedirs(dir_path, exist_ok=True)
        # 再帰的にフォルダを作成
        create_directory_recursive(dir_path, item[1:])

  # ルートディレクトリを作成
  os.makedirs(directory_structure[0], exist_ok=True)
  # 再帰的にディレクトリ構造を作成
  create_directory_recursive(directory_structure[0], directory_structure[1:])

# ディレクトリ構造を定義
directory_structure = [
  'youtube-subtitle-app',
  [
    'client',
    [
      'src',
      [
        'components',
        [
          'SearchForm.tsx',
          'SearchResultList.tsx',
          'SubtitleViewer.tsx'
        ],
        'pages',
        [
          'index.tsx',
          'subtitle',
          [
            '[videoId].tsx'
          ]
        ],
        'styles',
        [
          'globals.css',
          'tailwind.config.js'
        ],
        'public',
        [
          'index.html',
          'favicon.ico'
        ]
      ],
      'package.json'
    ],
    'server',
    [
      'app.py',
      'utils',
      [
        'youtube_api.py'
      ]
    ],
    'package.json'
  ]
]

# ディレクトリ構造を作成
create_directory_structure(directory_structure)
#