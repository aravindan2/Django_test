# Create your tests here.

import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Choice, Question


class QuestionModelTests(TestCase):
    def setUp(self):
        self.question = Question.objects.create(
            question_text="What is your favorite programming language?",
            pub_date=timezone.now() - datetime.timedelta(hours=1),
        )

    def test_question_str(self):
        self.assertEqual(
            str(self.question),
            "What is your favorite programming language?",
        )

    def test_was_published_recently_with_recent_question(self):
        self.assertTrue(self.question.was_published_recently())

    def test_was_published_recently_with_old_question(self):
        self.question.pub_date = timezone.now() - datetime.timedelta(days=2)
        self.question.save()

        self.assertFalse(self.question.was_published_recently())

    def test_was_published_recently_with_future_question(self):
        self.question.pub_date = timezone.now() + datetime.timedelta(days=1)
        self.question.save()

        self.assertFalse(self.question.was_published_recently())


class ChoiceModelTests(TestCase):
    def setUp(self):
        self.question = Question.objects.create(
            question_text="Choose a language",
            pub_date=timezone.now(),
        )
        self.choice = Choice.objects.create(
            question=self.question,
            choice_text="Python",
        )

    def test_choice_str(self):
        self.assertEqual(str(self.choice), "Python")

    def test_choice_default_votes_is_zero(self):
        self.assertEqual(self.choice.votes, 0)

    def test_question_can_have_multiple_choices(self):
        Choice.objects.create(
            question=self.question,
            choice_text="JavaScript",
        )

        self.assertEqual(self.question.choice_set.count(), 2)


class PollsViewTests(TestCase):
    def setUp(self):
        self.question = Question.objects.create(
            question_text="What is your favorite language?",
            pub_date=timezone.now() - datetime.timedelta(hours=1),
        )
        self.choice = Choice.objects.create(
            question=self.question,
            choice_text="Python",
        )

    def test_index_page_returns_200(self):
        response = self.client.get(reverse("polls:index"))

        self.assertEqual(response.status_code, 200)

    def test_index_page_displays_question(self):
        response = self.client.get(reverse("polls:index"))

        self.assertContains(response, self.question.question_text)

    def test_detail_page_returns_200(self):
        response = self.client.get(reverse("polls:detail", args=(self.question.pk,)))

        self.assertEqual(response.status_code, 200)

    def test_detail_page_displays_question(self):
        response = self.client.get(reverse("polls:detail", args=(self.question.pk,)))

        self.assertContains(response, self.question.question_text)

    def test_results_page_returns_200(self):
        response = self.client.get(reverse("polls:results", args=(self.question.pk,)))

        self.assertEqual(response.status_code, 200)

    def test_missing_question_returns_404(self):
        response = self.client.get(reverse("polls:detail", args=(99999,)))

        self.assertEqual(response.status_code, 404)

    def test_vote_increments_choice_votes(self):
        response = self.client.post(
            reverse("polls:vote", args=(self.question.pk,)),
            {"choice": self.choice.pk},
        )

        self.choice.refresh_from_db()

        self.assertEqual(self.choice.votes, 1)
        self.assertRedirects(
            response,
            reverse("polls:results", args=(self.question.pk,)),
        )

    def test_vote_without_choice_does_not_increment_votes(self):
        response = self.client.post(
            reverse("polls:vote", args=(self.question.pk,)),
            {},
        )

        self.choice.refresh_from_db()

        self.assertEqual(self.choice.votes, 0)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You didn't select a choice.")

    def test_vote_with_invalid_choice_does_not_increment_votes(self):
        response = self.client.post(
            reverse("polls:vote", args=(self.question.pk,)),
            {"choice": 99999},
        )

        self.choice.refresh_from_db()

        self.assertEqual(self.choice.votes, 0)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You didn't select a choice.")

    def test_voting_on_missing_question_returns_404(self):
        response = self.client.post(
            reverse("polls:vote", args=(99999,)),
            {"choice": self.choice.pk},
        )

        self.assertEqual(response.status_code, 404)
