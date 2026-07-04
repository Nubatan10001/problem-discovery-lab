from django.conf import settings
from django.db import models
from django.urls import reverse


class ProblemIdea(models.Model):
    class Status(models.TextChoices):
        UNEXPLORED = 'unexplored', '試作品未作成'
        RESEARCH = 'research', '研究候補'
        IMPLEMENTING = 'implementing', '実装中'
        IMPLEMENTED = 'implemented', '実装済み'
        BUSINESS = 'business', '事業化候補'

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='problem_ideas')
    title = models.CharField('課題タイトル', max_length=120, blank=True)
    raw_memo = models.TextField('違和感メモ')
    category = models.CharField('カテゴリ', max_length=60, blank=True)
    status = models.CharField('ステータス', max_length=20, choices=Status.choices, default=Status.UNEXPLORED)
    target_user = models.CharField('対象ユーザー', max_length=160, blank=True)
    core_problem = models.TextField('本質的課題', blank=True)
    mvp_plan = models.TextField('最初の試作品案', blank=True)
    research_theme = models.TextField('研究テーマ候補', blank=True)
    business_potential = models.TextField('事業化可能性', blank=True)
    structured_data = models.JSONField('AI構造化データ', default=dict, blank=True)
    created_at = models.DateTimeField('作成日', auto_now_add=True)
    updated_at = models.DateTimeField('更新日', auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = '課題アイデア'
        verbose_name_plural = '課題アイデア'

    def __str__(self):
        return self.display_title

    @property
    def display_title(self):
        return self.title or self.raw_memo[:32]

    def get_absolute_url(self):
        return reverse('problem_detail', kwargs={'pk': self.pk})


class ConversationMessage(models.Model):
    class Role(models.TextChoices):
        USER = 'user', 'ユーザー'
        ASSISTANT = 'assistant', 'AI'

    idea = models.ForeignKey(ProblemIdea, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField('発言者', max_length=20, choices=Role.choices)
    content = models.TextField('内容')
    created_at = models.DateTimeField('作成日', auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = '会話メッセージ'
        verbose_name_plural = '会話メッセージ'

    def __str__(self):
        return f'{self.get_role_display()}: {self.content[:30]}'

# Create your models here.
