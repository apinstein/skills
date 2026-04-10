#!/usr/bin/env python3
"""
Tests for parse_threads() in the reviewable script.

Fixtures are markdown files in tests/fixtures/ that simulate real GitHub API payloads.
Each test builds synthetic items (as fetch_comments would produce) and asserts on
the output of parse_threads().
"""

import sys
import os
import importlib
import importlib.util
import importlib.machinery
import pytest

# Allow importing the reviewable script directly (it has no .py extension)
_script_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "reviewable")
spec = importlib.util.spec_from_loader("reviewable", importlib.machinery.SourceFileLoader("reviewable", _script_path))
reviewable = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reviewable)
parse_threads = reviewable.parse_threads
_print_thread = reviewable._print_thread
AI_SIGNATURE = reviewable.AI_SIGNATURE

FIXTURES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")

def load_fixture(name):
    with open(os.path.join(FIXTURES, name)) as f:
        return f.read()

def make_review(body, user="reviewer", ts="2024-01-01T10:00:00Z"):
    return {'id': 1, 'body': body, 'user': user, 'created_at': ts, 'type': 'review'}

def make_comment(body, user="commenter", ts="2024-01-01T11:00:00Z"):
    return {'id': 2, 'body': body, 'user': user, 'created_at': ts, 'type': 'comment'}


# ---------------------------------------------------------------------------
# 1. Batch split: review body with 3 threads → exactly 1 history entry each
# ---------------------------------------------------------------------------

class TestBatchReviewSplit:
    def setup_method(self):
        self.review_body = load_fixture("review_1.md")
        self.items = [make_review(self.review_body)]
        self.threads = parse_threads(self.items)

    def test_discovers_all_three_threads(self):
        assert "-ThreadA" in self.threads
        assert "-ThreadB" in self.threads
        assert "-ThreadC" in self.threads

    def test_each_thread_has_exactly_one_history_entry(self):
        assert len(self.threads["-ThreadA"]["history"]) == 1
        assert len(self.threads["-ThreadB"]["history"]) == 1
        assert len(self.threads["-ThreadC"]["history"]) == 1

    def test_thread_a_body_contains_only_thread_a_content(self):
        body = self.threads["-ThreadA"]["history"][0]["body"]
        assert "hardcoded" in body          # Thread A's text
        assert "cached" not in body         # Thread B's text absent
        assert "dangerous" not in body      # Thread C's text absent

    def test_thread_b_body_contains_only_thread_b_content(self):
        body = self.threads["-ThreadB"]["history"][0]["body"]
        assert "cached" in body
        assert "hardcoded" not in body
        assert "dangerous" not in body

    def test_thread_c_body_contains_only_thread_c_content(self):
        body = self.threads["-ThreadC"]["history"][0]["body"]
        assert "dangerous" in body
        assert "hardcoded" not in body
        assert "cached" not in body

    def test_status_is_action_required_with_no_ai_reply(self):
        # No AI replies yet — all threads need attention
        for tid in ["-ThreadA", "-ThreadB", "-ThreadC"]:
            assert self.threads[tid]["status"] == "action_required", \
                f"Thread {tid} should be action_required"


# ---------------------------------------------------------------------------
# 2. Issue comment routing: reply goes only to the correct thread
# ---------------------------------------------------------------------------

class TestIssueCommentRouting:
    def setup_method(self):
        review_body = load_fixture("review_1.md")
        ai_reply = load_fixture("issue_comment_thread_a_ai_reply.md")
        self.items = [
            make_review(review_body, ts="2024-01-01T10:00:00Z"),
            make_comment(ai_reply, user="ai-bot", ts="2024-01-01T11:00:00Z"),
        ]
        self.threads = parse_threads(self.items)

    def test_thread_a_has_two_history_entries(self):
        # Review section + AI reply
        assert len(self.threads["-ThreadA"]["history"]) == 2

    def test_thread_b_and_c_unchanged(self):
        assert len(self.threads["-ThreadB"]["history"]) == 1
        assert len(self.threads["-ThreadC"]["history"]) == 1

    def test_thread_a_last_entry_is_ai_reply(self):
        last = self.threads["-ThreadA"]["history"][-1]
        assert AI_SIGNATURE in last["body"]


# ---------------------------------------------------------------------------
# 3. Status logic: list and thread views
# ---------------------------------------------------------------------------

class TestStatusAndListView:
    def setup_method(self):
        review_body = load_fixture("review_1.md")
        ai_reply_a = load_fixture("issue_comment_thread_a_ai_reply.md")
        human_followup_b = load_fixture("issue_comment_thread_b_human_followup.md")
        self.items = [
            make_review(review_body, ts="2024-01-01T10:00:00Z"),
            make_comment(ai_reply_a, user="ai-bot", ts="2024-01-01T11:00:00Z"),
            make_comment(human_followup_b, user="reviewer", ts="2024-01-01T12:00:00Z"),
        ]
        self.threads = parse_threads(self.items)

    def test_thread_a_is_addressed(self):
        # AI replied last → addressed, should NOT appear in `list`
        assert self.threads["-ThreadA"]["status"] == "addressed"

    def test_thread_b_is_action_required(self):
        # Human followed up after AI → action_required, should appear in `list`
        assert self.threads["-ThreadB"]["status"] == "action_required"

    def test_thread_c_is_action_required(self):
        # No reply at all → action_required
        assert self.threads["-ThreadC"]["status"] == "action_required"

    def test_thread_b_last_snippet_is_human_followup(self):
        # The snippet is the first 80 chars of the last history entry's body.
        # The human followup starts with the quoted header then the reply text.
        last = self.threads["-ThreadB"]["history"][-1]
        assert "O(1)" in last["body"]          # full body has the text
        assert "-ThreadB" in last["body"]      # and it references thread B

    def test_thread_a_view_shows_both_entries(self):
        history = self.threads["-ThreadA"]["history"]
        assert len(history) == 2
        bodies = [h["body"] for h in history]
        assert any("hardcoded" in b for b in bodies)     # opener
        assert any(AI_SIGNATURE in b for b in bodies)   # AI reply

    def test_thread_b_view_shows_both_entries(self):
        history = self.threads["-ThreadB"]["history"]
        assert len(history) == 2
        bodies = [h["body"] for h in history]
        assert any("cached" in b for b in bodies)        # opener
        assert any("O(1)" in b for b in bodies)          # human followup


# ---------------------------------------------------------------------------
# 4. _print_thread output: list command emits full content inline
# ---------------------------------------------------------------------------

class TestPrintThreadOutput:
    def setup_method(self):
        review_body = load_fixture("review_1.md")
        ai_reply = load_fixture("issue_comment_thread_a_ai_reply.md")
        items = [
            make_review(review_body, ts="2024-01-01T10:00:00Z"),
            make_comment(ai_reply, user="ai-bot", ts="2024-01-01T11:00:00Z"),
        ]
        self.threads = parse_threads(items)

    def test_print_thread_includes_thread_id_and_header(self, capsys):
        _print_thread("-ThreadA", self.threads["-ThreadA"])
        out = capsys.readouterr().out
        assert "-ThreadA" in out
        assert "src/foo.swift" in out   # file from header

    def test_print_thread_includes_all_history_bodies(self, capsys):
        _print_thread("-ThreadA", self.threads["-ThreadA"])
        out = capsys.readouterr().out
        assert "hardcoded" in out       # opener text
        assert AI_SIGNATURE in out      # AI reply
