from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.db import transaction
from .models import Poll, Option, Vote
from .forms import CreatePollForm

def _ensure_session(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key

def poll_list(request):
    polls = Poll.objects.order_by("-created_at")
    return render(request, "polls/poll_list.html", {"polls": polls})

def poll_detail(request, pk):
    poll = get_object_or_404(Poll, pk=pk, is_active=True)
    if request.method == "POST":
        session_key = _ensure_session(request)
        option_id = request.POST.get("option")
        option = get_object_or_404(Option, pk=option_id, poll=poll)

        try:
            with transaction.atomic():
                Vote.objects.create(
                    poll=poll,
                    option=option,
                    user=request.user if request.user.is_authenticated else None,
                    session_key=None if request.user.is_authenticated else session_key,
                )
            messages.success(request, "Your vote has been recorded!")
        except Exception as e:
            messages.warning(request, "You have already voted in this poll.")
        return redirect(reverse("poll_detail", args=[poll.pk]))

    # For results, compute percentages
    total = poll.total_votes or 1  # avoid div by zero
    options = [
        {"obj": o, "count": o.votes_count, "pct": int((o.votes_count / total) * 100)}
        for o in poll.options.all()
    ]
    # Check if user/session already voted
    session_key = request.session.session_key
    voted = False
    if request.user.is_authenticated:
        voted = Vote.objects.filter(poll=poll, user=request.user).exists()
    elif session_key:
        voted = Vote.objects.filter(poll=poll, session_key=session_key).exists()

    return render(request, "polls/poll_detail.html", {"poll": poll, "options": options, "voted": voted})

def create_poll(request):
    if request.method == "POST":
        form = CreatePollForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            options = form.cleaned_data["clean_options_text"] if "clean_options_text" in form.cleaned_data else form.cleaned_data["options_text"]
            poll = Poll.objects.create(title=title, description=description, created_by=request.user if request.user.is_authenticated else None)
            for text in options:
                Option.objects.create(poll=poll, text=text)
            messages.success(request, "Poll created!")
            return redirect("poll_detail", pk=poll.pk)
    else:
        form = CreatePollForm()
    return render(request, "polls/create_poll.html", {"form": form})
