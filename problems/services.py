import json
import os

from django.conf import settings
from openai import OpenAI


DISCOVERY_SYSTEM_PROMPT = """
あなたはデザイン思考、研究テーマ設計、AIプロダクト企画に強い壁打ち相手です。
ユーザーの日常の違和感を、課題発見、最初の試作品案、研究テーマ、事業化可能性へ育てます。
質問は一度に3つまでに絞り、初心者にも答えやすい日本語で返してください。
"""

STRUCTURE_SYSTEM_PROMPT = """
あなたはAI Problem Discovery Labの構造化エンジンです。
会話内容をもとに、課題発見から実装・研究・事業化までを整理してください。
必ずJSONだけを返してください。
"""

STRUCTURE_KEYS = [
    'title',
    'target_user',
    'situation',
    'core_problem',
    'current_solution',
    'unsolved_reason',
    'ai_app_solution',
    'mvp_plan',
    'similar_apps_or_research',
    'evaluation_metrics',
    'research_theme',
    'business_potential',
]


def has_openai_key():
    return bool(os.getenv('OPENAI_API_KEY'))


def generate_followup_question(idea, messages):
    if not has_openai_key():
        return _fallback_question(idea, messages)

    client = OpenAI()
    conversation = [{'role': 'system', 'content': DISCOVERY_SYSTEM_PROMPT}]
    conversation.append({'role': 'user', 'content': f'最初の違和感メモ: {idea.raw_memo}'})
    for message in messages:
        conversation.append({'role': message.role, 'content': message.content})
    conversation.append({
        'role': 'user',
        'content': 'この課題を深掘りするための次の質問をしてください。必要なら仮説も1つ添えてください。',
    })

    response = client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=conversation,
        temperature=0.4,
    )
    return response.choices[0].message.content.strip()


def structure_problem(idea, messages):
    if not has_openai_key():
        return _fallback_structure(idea, messages)

    transcript = '\n'.join([
        f'{message.get_role_display()}: {message.content}'
        for message in messages
    ])
    user_prompt = f"""
最初の違和感メモ:
{idea.raw_memo}

会話ログ:
{transcript}

以下のキーを持つJSONで整理してください:
{', '.join(STRUCTURE_KEYS)}
"""
    response = client_response_as_json(user_prompt)
    return {key: response.get(key, '') for key in STRUCTURE_KEYS}


def client_response_as_json(user_prompt):
    client = OpenAI()
    response = client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[
            {'role': 'system', 'content': STRUCTURE_SYSTEM_PROMPT},
            {'role': 'user', 'content': user_prompt},
        ],
        response_format={'type': 'json_object'},
        temperature=0.2,
    )
    content = response.choices[0].message.content
    return json.loads(content)


def apply_structure_to_idea(idea, data):
    idea.structured_data = data
    idea.title = data.get('title', idea.title)
    idea.target_user = data.get('target_user', idea.target_user)
    idea.core_problem = data.get('core_problem', idea.core_problem)
    idea.mvp_plan = data.get('mvp_plan', idea.mvp_plan)
    idea.research_theme = data.get('research_theme', idea.research_theme)
    idea.business_potential = data.get('business_potential', idea.business_potential)
    idea.save()
    return idea


def _fallback_question(idea, messages):
    question_sets = [
        '誰が一番困っていましたか？その人はどんな状況で困っていましたか？',
        'その違和感はどのくらいの頻度で起こりますか？1回あたり何分くらい失っていますか？',
        '今はどんな方法で対処していますか？その方法の不満は何ですか？',
        'AIやアプリが関わるなら、判断・要約・検索・自動化のどれが一番効きそうですか？',
        '最初の試作品として、1週間で作るなら何ができれば価値を感じますか？',
    ]
    index = min(messages.filter(role='assistant').count(), len(question_sets) - 1)
    return question_sets[index]


def _fallback_structure(idea, messages):
    user_notes = ' / '.join(
        message.content for message in messages if message.role == 'user'
    )
    memo = idea.raw_memo
    return {
        'title': memo[:40],
        'target_user': 'この違和感を日常的に経験している人',
        'situation': memo,
        'core_problem': f'まだ仮説段階です。追加メモ: {user_notes or "未入力"}',
        'current_solution': '手作業、既存メモ、個人の工夫で対処している可能性があります。',
        'unsolved_reason': '困りごとが小さく見えやすく、課題として構造化されていないため。',
        'ai_app_solution': 'AIが質問し、課題・利用者・最初の試作品・研究テーマを整理する支援が考えられます。',
        'mvp_plan': '違和感メモ登録、AI質問、構造化結果保存、一覧管理までを最初の試作品にします。',
        'similar_apps_or_research': 'Notion、メモアプリ、アイデア管理ツール、LLMリフレクション研究を調査候補にします。',
        'evaluation_metrics': '削減時間、課題定義の明確さ、試作品案の具体性、研究テーマ化できた件数。',
        'research_theme': 'LLMとの対話型リフレクションが課題発見能力に与える影響。',
        'business_potential': '学生、研究者、起業準備者、新規事業担当者向けの課題発見支援ツールとして検証可能です。',
    }
