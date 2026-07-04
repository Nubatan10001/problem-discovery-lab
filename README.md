# AI Problem Discovery Lab

日常の違和感メモをAIとの壁打ちで深掘りし、課題、最初の試作品案、研究テーマ、事業化可能性へ整理するDjangoアプリです。

## できること

- ユーザー登録とログイン
- 違和感メモの投稿
- AIとの壁打ち形式の質問
- 会話内容から課題を構造化
- 課題一覧、詳細表示、検索、カテゴリ/ステータス管理
- SQLiteへの保存

## 起動方法

```bash
cd ~/Desktop/02_開発用フォルダ/02_実装提案アプリ
source venv/bin/activate
python manage.py runserver
```

ブラウザで http://127.0.0.1:8000/ を開きます。

## OpenAI APIキーを使う場合

`.env.example` を参考に `.env` を作成し、`OPENAI_API_KEY` を設定してください。

```bash
cp .env.example .env
```

APIキーが未設定でも、開発確認用の仮質問と仮構造化が動きます。

## テスト

```bash
source venv/bin/activate
python manage.py test
```
