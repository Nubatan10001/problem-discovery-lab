from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import ConversationMessage, ProblemIdea
from .services import apply_structure_to_idea, structure_problem


class ProblemIdeaTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='founder', password='pass-test-123')

    def test_authenticated_user_can_create_problem_idea(self):
        self.client.login(username='founder', password='pass-test-123')
        with patch.dict('os.environ', {'OPENAI_API_KEY': ''}):
            response = self.client.post(reverse('problem_create'), {
                'raw_memo': '会議後に議事録を書くのが面倒だった。',
                'category': '業務効率化',
                'status': ProblemIdea.Status.UNEXPLORED,
            })

        idea = ProblemIdea.objects.get()
        self.assertRedirects(response, idea.get_absolute_url())
        self.assertEqual(idea.owner, self.user)
        self.assertEqual(idea.messages.filter(role=ConversationMessage.Role.ASSISTANT).count(), 1)

    def test_fallback_structure_updates_idea(self):
        idea = ProblemIdea.objects.create(
            owner=self.user,
            raw_memo='研究テーマが散らばって整理できない。',
            category='研究',
        )
        ConversationMessage.objects.create(
            idea=idea,
            role=ConversationMessage.Role.USER,
            content='大学院の研究計画に使いたい。',
        )

        with patch.dict('os.environ', {'OPENAI_API_KEY': ''}):
            data = structure_problem(idea, idea.messages.all())
        apply_structure_to_idea(idea, data)
        idea.refresh_from_db()

        self.assertTrue(idea.title)
        self.assertTrue(idea.mvp_plan)
        self.assertIn('research_theme', idea.structured_data)

# Create your tests here.
