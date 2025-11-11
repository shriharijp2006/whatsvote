from django.db import models
from django.contrib.auth.models import User

class Poll(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    @property
    def total_votes(self):
        return Vote.objects.filter(poll=self).count()

class Option(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="options")
    text = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.poll.title} - {self.text}"

    @property
    def votes_count(self):
        return Vote.objects.filter(option=self).count()

class Vote(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="votes")
    option = models.ForeignKey(Option, on_delete=models.CASCADE, related_name="votes")
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["poll", "user"], name="unique_user_vote", condition=models.Q(user__isnull=False)),
            models.UniqueConstraint(fields=["poll", "session_key"], name="unique_session_vote", condition=models.Q(session_key__isnull=False)),
        ]

    def __str__(self):
        who = self.user.username if self.user else f"session:{self.session_key}"
        return f"Vote({self.poll_id} -> {self.option_id}) by {who}"
