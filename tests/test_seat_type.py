from smartsheet.models import User, UserPlan
from smartsheet.models.enums import SeatType, DowngradeSeatType


def test_seat_type_members():
    assert [m.value for m in SeatType] == ['GUEST', 'MEMBER', 'PROVISIONAL_MEMBER', 'CONTRIBUTOR']


def test_downgrade_seat_type_members():
    assert [m.value for m in DowngradeSeatType] == ['GUEST', 'CONTRIBUTOR']


def test_user_plan_viewer_seat_type_reads_as_none():
    plan = UserPlan({'planId': 1, 'seatType': 'VIEWER'})
    assert plan.plan_id == 1
    assert plan.seat_type.value is None


def test_user_viewer_seat_type_reads_as_none():
    assert User({'id': 1, 'seatType': 'VIEWER'}).seat_type.value is None
