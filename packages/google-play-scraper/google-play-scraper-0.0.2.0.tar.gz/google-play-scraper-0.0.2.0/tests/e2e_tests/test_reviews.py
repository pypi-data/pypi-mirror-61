from datetime import datetime
from unittest import TestCase

from google_play_scraper import reviews, Sort


class TestApp(TestCase):
    def test_e2e_scenario_1(self):
        result = reviews("com.mojang.minecraftpe", sort=Sort.NEWEST, count=500)

        self.assertEqual(500, len(result))

        review_created_version_contained_review_count = 0

        for r in result:
            self.assertTrue(r["userName"])
            self.assertTrue(r["userImage"])
            self.assertTrue(r["content"])
            self.assertTrue(r["score"] >= 1)
            self.assertTrue(r["thumbsUpCount"] >= 0)
            self.assertTrue(datetime(2019, 12, 1) < r["at"] < datetime(2040, 1, 1))

            if r["reviewCreatedVersion"]:
                review_created_version_contained_review_count += 1

        self.assertTrue(review_created_version_contained_review_count > 100)

        last_review_at = result[0]["at"]
        well_sorted_review_count = 0

        for r in result[1:]:
            review_at = r["at"]

            if review_at <= last_review_at:
                well_sorted_review_count += 1

            last_review_at = review_at

        self.assertTrue(well_sorted_review_count > 490)

    def test_e2e_scenario_2(self):
        result = reviews("com.mojang.minecraftpe", sort=Sort.MOST_RELEVANT, count=20)

        self.assertEqual(20, len(result))

        for r in result:
            self.assertTrue(0 < r["thumbsUpCount"])

    def test_e2e_scenario_3(self):
        result = reviews("com.mojang.minecraftpe", sort=Sort.RATING, count=100)

        self.assertEqual(100, len(result))

        for r in result:
            self.assertEqual(5, r["score"])
