from django.db import models


class GameReview(models.Model):
    game_name = models.CharField(max_length=255)
    game_review = models.TextField()
    game_rating = models.IntegerField()
    image = models.ImageField(upload_to='game_images/', null=True, blank=True)


    def __str__(self):
        return self.game_name
