"""
A resolution that matches using equality. Resolutions must be paired with
questions and passed together to an actor like so:

    the_actor.should_see_the((Number.of_the(TODO_ITEMS), IsEqualTo(4)))
"""


from hamcrest import equal_to

from .base_resolution import Resolution


class IsEqualTo(Resolution):
    """
    Matches on equality (i.e. `a == b`).
    """

    expected: object
    matcher: object

    line = "to find {expectation}"

    def __init__(self, obj: object) -> None:
        self.expected = obj
        self.matcher = equal_to(obj)
