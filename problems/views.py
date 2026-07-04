from django.contrib import messages as django_messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ConversationMessageForm, ProblemIdeaForm, SignUpForm
from .models import ConversationMessage, ProblemIdea
from .services import apply_structure_to_idea, generate_followup_question, structure_problem


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('problem_list')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def problem_list(request):
    ideas = ProblemIdea.objects.filter(owner=request.user)
    query = request.GET.get('q', '').strip()
    status = request.GET.get('status', '').strip()
    category = request.GET.get('category', '').strip()

    if query:
        ideas = ideas.filter(
            Q(title__icontains=query)
            | Q(raw_memo__icontains=query)
            | Q(core_problem__icontains=query)
            | Q(mvp_plan__icontains=query)
            | Q(research_theme__icontains=query)
        )
    if status:
        ideas = ideas.filter(status=status)
    if category:
        ideas = ideas.filter(category__icontains=category)

    context = {
        'ideas': ideas,
        'query': query,
        'selected_status': status,
        'category': category,
        'status_choices': ProblemIdea.Status.choices,
    }
    return render(request, 'problems/problem_list.html', context)


@login_required
def problem_create(request):
    if request.method == 'POST':
        form = ProblemIdeaForm(request.POST)
        if form.is_valid():
            idea = form.save(commit=False)
            idea.owner = request.user
            idea.save()
            try:
                question = generate_followup_question(idea, idea.messages.all())
            except Exception as exc:
                question = 'まず、誰がどんな状況で一番困っているのか教えてください。'
                django_messages.warning(request, f'AI呼び出しに失敗したため、仮の質問を表示しました: {exc}')
            ConversationMessage.objects.create(
                idea=idea,
                role=ConversationMessage.Role.ASSISTANT,
                content=question,
            )
            django_messages.success(request, '課題メモを保存しました。AIとの壁打ちを始めましょう。')
            return redirect(idea)
    else:
        form = ProblemIdeaForm()
    return render(request, 'problems/problem_form.html', {'form': form})


@login_required
def problem_detail(request, pk):
    idea = get_object_or_404(ProblemIdea, pk=pk, owner=request.user)
    form = ConversationMessageForm()
    return render(request, 'problems/problem_detail.html', {'idea': idea, 'form': form})


@login_required
def add_message(request, pk):
    idea = get_object_or_404(ProblemIdea, pk=pk, owner=request.user)
    if request.method != 'POST':
        return redirect(idea)

    form = ConversationMessageForm(request.POST)
    if form.is_valid():
        ConversationMessage.objects.create(
            idea=idea,
            role=ConversationMessage.Role.USER,
            content=form.cleaned_data['content'],
        )
        try:
            question = generate_followup_question(idea, idea.messages.all())
        except Exception as exc:
            question = 'ありがとうございます。次に、この課題が解決されたら何がどれくらい良くなるか教えてください。'
            django_messages.warning(request, f'AI呼び出しに失敗したため、仮の質問を表示しました: {exc}')
        ConversationMessage.objects.create(
            idea=idea,
            role=ConversationMessage.Role.ASSISTANT,
            content=question,
        )
        django_messages.success(request, '返信を保存し、次の質問を追加しました。')
    return redirect(idea)


@login_required
def structure_idea(request, pk):
    idea = get_object_or_404(ProblemIdea, pk=pk, owner=request.user)
    if request.method == 'POST':
        try:
            data = structure_problem(idea, idea.messages.all())
            apply_structure_to_idea(idea, data)
            django_messages.success(request, 'AI構造化を保存しました。')
        except Exception as exc:
            django_messages.error(request, f'AI構造化に失敗しました: {exc}')
    return redirect(idea)

# Create your views here.
