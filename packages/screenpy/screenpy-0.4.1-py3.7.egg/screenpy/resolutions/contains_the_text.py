"""
A resolution that matches against a substring. Resolutions must be paired
with questions and passed together to an actor like so:

    the_actor.should_see_the(
        (Text.of_the(WELCOME_BANNER), ContainsTheText("Welcome!")),
    )
"""


from hamcrest import contains_string

from .base_resolution import Resolution


class ContainsTheText(Resolution):
    """
    Matches a substring (e.g. `"play" in "screenplay"`).
    """

    expected: str
    matcher: object

    line = 'to have "{expectation}"'

    def __init__(self, substring: str) -> None:
        self.expected = substring
        self.matcher = contains_string(substring)
