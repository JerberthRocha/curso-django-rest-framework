from unittest import TestCase
from utils.pagination import make_pagination_range


class PaginationTest(TestCase):
    def test_make_pagination_range_returns_a_pagination_range(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 6)),
            qty_pages=4,
            current_page=1,
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)

    def test_first_range_is_static__if_current_page_is_less_than_middle_page(self):
        # Current page = 1 - Qty page = 2 - Middle page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 6)),
            qty_pages=4,
            current_page=1,
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)

        # Current page = 2 - Qty page = 2 - Middle page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 6)),
            qty_pages=4,
            current_page=2,
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)

        # Current page = 3 - Qty page = 2 - Middle page = 2
        # HERE RANGE SHOULD CHANGE
        # pagination = make_pagination_range(
        #     page_range=list(range(1, 6)),
        #     qty_pages=4,
        #     current_page=3,
        # )
        # self.assertEqual([2, 3, 4, 5], pagination)

    def test_make_sure_middle_ranges_are_corrects(self):
        # Current page = 3 - Qty page = 2 - Middle page = 2
        # HERE RANGE SHOULD CHANGE
        pagination = make_pagination_range(
            page_range=list(range(1, 6)),
            qty_pages=4,
            current_page=3,
        )['pagination']
        self.assertEqual([2, 3, 4, 5], pagination)

    def test_make_pagination_range_is_static_when_last_page_is_next(self):
         # Current page = 3 - Qty page = 2 - Middle page = 2
        # HERE RANGE SHOULD CHANGE
        pagination = make_pagination_range(
            page_range=list(range(1, 6)),
            qty_pages=4,
            current_page=3,
        )['pagination']
        self.assertEqual([2, 3, 4, 5], pagination)

        # Current page = 4 - Qty page = 2 - Middle page = 2
        # HERE RANGE SHOULD CHANGE
        pagination = make_pagination_range(
            page_range=list(range(1, 6)),
            qty_pages=4,
            current_page=4,
        )['pagination']
        self.assertEqual([2, 3, 4, 5], pagination)
