"""
Unit tests for the gamification calculator functions in app.py.

Run with:  pytest test_calculator.py -v
"""

import os
import pytest
import flask

# Both env vars must be set before app.py is imported (module-level guards).
os.environ.setdefault("ANTHROPIC_API_KEY", "test-key")
os.environ.setdefault("FLASK_SECRET_KEY", "test-secret")

from app import app, get_user_level, get_xp_for_next_level, add_xp, XP_LEVELS


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_user(tier="free", xp=0, level=1):
    """Return a minimal user_progress dict suitable for seeding the session."""
    return {
        "xp": xp,
        "level": level,
        "subscription_tier": tier,
        "subscription_expires": None,
        "is_developer": False,
        "sections_unlocked": ["home", "paiboon", "learn", "alphabet"],
        "sections_visited": [],
        "achievements_earned": [],
        "quizzes_completed": 0,
        "quiz_perfect_count": 0,
        "words_learned": 0,
        "correct_answers": 0,
        "total_answers": 0,
        "login_streak": 1,
        "last_login": "2026-01-01T00:00:00",
        "daily_points_earned": 0,
        "alphabet_completed": False,
        "alphabet_completion_date": None,
    }


# ---------------------------------------------------------------------------
# get_user_level
# ---------------------------------------------------------------------------

class TestGetUserLevel:
    def test_zero_xp_is_level_1(self):
        assert get_user_level(0) == 1

    def test_just_below_level_2_threshold(self):
        assert get_user_level(99) == 1

    def test_exactly_at_level_2_threshold(self):
        assert get_user_level(100) == 2

    def test_midway_through_level_2(self):
        assert get_user_level(175) == 2

    def test_just_below_level_3_threshold(self):
        assert get_user_level(249) == 2

    def test_exactly_at_level_3_threshold(self):
        assert get_user_level(250) == 3

    def test_exactly_at_level_5_threshold(self):
        assert get_user_level(1000) == 5

    def test_exactly_at_level_10_threshold(self):
        assert get_user_level(12000) == 10

    def test_xp_beyond_max_level_capped_at_10(self):
        assert get_user_level(999_999) == 10

    def test_each_xp_level_threshold_returns_correct_level(self):
        """Boundary check: every entry in XP_LEVELS resolves to its key."""
        for level, xp in XP_LEVELS.items():
            assert get_user_level(xp) == level, (
                f"Expected level {level} for {xp} XP, got {get_user_level(xp)}"
            )


# ---------------------------------------------------------------------------
# get_xp_for_next_level
# ---------------------------------------------------------------------------

class TestGetXpForNextLevel:
    def test_level_1_requires_100_for_next(self):
        assert get_xp_for_next_level(1) == 100

    def test_level_2_requires_250_for_next(self):
        assert get_xp_for_next_level(2) == 250

    def test_level_9_requires_12000_for_next(self):
        assert get_xp_for_next_level(9) == 12000

    def test_max_level_returns_none(self):
        assert get_xp_for_next_level(10) is None

    def test_all_non_max_levels_match_xp_levels_dict(self):
        for level in range(1, 10):
            assert get_xp_for_next_level(level) == XP_LEVELS[level + 1]


# ---------------------------------------------------------------------------
# add_xp  (requires a Flask request context for session access)
# ---------------------------------------------------------------------------

class TestAddXp:
    def setup_method(self):
        app.config["TESTING"] = True

    def _call(self, points, tier="free", xp=0, level=1, description=""):
        """Push a request context, seed the session, call add_xp, return result."""
        with app.test_request_context("/"):
            flask.session["user_progress"] = make_user(tier=tier, xp=xp, level=level)
            return add_xp(points, description)

    # -- multiplier tests --

    def test_free_tier_applies_1x_multiplier(self):
        result = self._call(10, tier="free")
        assert result["points_earned"] == 10

    def test_basic_tier_applies_2x_multiplier(self):
        result = self._call(10, tier="basic")
        assert result["points_earned"] == 20

    def test_pro_tier_applies_3x_multiplier(self):
        result = self._call(10, tier="pro")
        assert result["points_earned"] == 30

    def test_fractional_points_truncated_to_int(self):
        # 5 points × 2 = 10 (no fractions here), but using odd numbers:
        result = self._call(7, tier="basic")  # 7 × 2 = 14
        assert isinstance(result["points_earned"], int)
        assert result["points_earned"] == 14

    # -- xp accumulation --

    def test_points_added_to_existing_xp(self):
        result = self._call(50, tier="free", xp=200)
        assert result["total_xp"] == 250

    def test_multiplied_points_added_to_existing_xp(self):
        result = self._call(10, tier="pro", xp=100)  # 10 × 3 = 30
        assert result["total_xp"] == 130

    # -- level-up detection --

    def test_level_up_detected_when_xp_crosses_threshold(self):
        # 90 XP + 10 = 100 → crosses the level-2 threshold
        result = self._call(10, tier="free", xp=90, level=1)
        assert result["level_up"] is True
        assert result["level"] == 2

    def test_no_level_up_when_staying_in_same_level(self):
        result = self._call(5, tier="free", xp=0, level=1)
        assert result["level_up"] is False
        assert result["level"] == 1

    def test_multiple_levels_crossed_in_one_call(self):
        # Jump from 0 XP to 500 XP in one shot (crosses levels 2, 3, 4)
        result = self._call(500, tier="free", xp=0, level=1)
        assert result["level"] == 4
        assert result["level_up"] is True

    # -- return value shape --

    def test_action_description_echoed_in_result(self):
        result = self._call(10, description="quiz correct")
        assert result["action"] == "quiz correct"

    def test_result_contains_all_expected_keys(self):
        result = self._call(10)
        assert set(result.keys()) == {
            "points_earned", "total_xp", "level", "level_up", "action"
        }


# ---------------------------------------------------------------------------
# Progress-to-next-level percentage (inline logic from progress_dashboard)
# ---------------------------------------------------------------------------

class TestProgressPercentage:
    """
    The percentage calculation lives inline in progress_dashboard().
    These tests verify the formula in isolation.
    """

    def _calc(self, user_xp, current_level):
        next_xp = get_xp_for_next_level(current_level)
        current_xp = XP_LEVELS[current_level]
        if next_xp is not None:
            return ((user_xp - current_xp) / (next_xp - current_xp)) * 100
        return 100

    def test_zero_progress_at_exact_level_start(self):
        assert self._calc(0, 1) == 0.0

    def test_fifty_percent_at_midpoint_of_level(self):
        # Level 1: 0 → 100; midpoint = 50 XP → 50 %
        assert self._calc(50, 1) == 50.0

    def test_full_progress_at_max_level(self):
        assert self._calc(12000, 10) == 100

    def test_zero_progress_at_start_of_level_2(self):
        assert self._calc(100, 2) == 0.0

    def test_progress_never_exceeds_100_within_level(self):
        # Just below level 3 threshold while still in level 2
        pct = self._calc(249, 2)
        assert 0 <= pct < 100

    def test_progress_increases_with_more_xp(self):
        pct_low = self._calc(25, 1)
        pct_high = self._calc(75, 1)
        assert pct_low < pct_high
