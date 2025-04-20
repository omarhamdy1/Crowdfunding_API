from django.db import models
from django.contrib.auth.models import User


class Collect(models.Model):
    OCCASION_CHOICES = (
        ('birthday', 'День рождения'),
        ('wedding', 'Свадьба'),
        ('charity', 'Благотворительность'),
        ('other', 'Другое'),
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='collects'
    )
    title = models.CharField(max_length=255)
    occasion = models.CharField(max_length=20, choices=OCCASION_CHOICES)
    description = models.TextField()
    target_amount = models.IntegerField(default=0)
    collected_amount = models.IntegerField(default=0)
    donors_count = models.IntegerField(default=0)
    cover_image = models.ImageField(
        upload_to='collect_covers/',
        null=True,
        blank=True
    )
    end_date = models.DateTimeField()

    def __str__(self):
        return self.title


class Payment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='payments'
    )
    collect = models.ForeignKey(
        Collect,
        on_delete=models.CASCADE,
        related_name='payments'
    )
    amount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.amount}'
