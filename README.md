# AI Problem Discovery Lab

日常の違和感メモをAIとの壁打ちで深掘りし、課題、最初の試作品案、研究テーマ、事業化可能性へ整理するDjangoアプリです。

## 公開範囲について

このリポジトリには、アプリケーションのソースコードとセットアップに必要な情報のみを置きます。

APIキー、`.env`、ローカルDB、仮想環境、個人用の開発メモはコミットしません。

## できること

- ユーザー登録とログイン
- 違和感メモの投稿
- AIとの壁打ち形式の質問
- 会話内容から課題を構造化
- 課題一覧、詳細表示、検索、カテゴリ/ステータス管理
- SQLiteへの保存

## 起動方法

```bash
git clone https://github.com/Nubatan10001/problem-discovery-lab.git
cd problem-discovery-lab
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

ブラウザで http://127.0.0.1:8000/ を開きます。

## OpenAI APIキーを使う場合

`.env.example` を参考に `.env` を作成し、`OPENAI_API_KEY` を設定してください。

```bash
cp .env.example .env
```

APIキーが未設定でも、開発確認用の仮質問と仮構造化が動きます。

`.env` は公開しないでください。

## テスト

```bash
source venv/bin/activate
python manage.py test
```
