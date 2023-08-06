"""
Resolutions provide the expected answers to Questions. All Resolutions
are given the expected value when instantiated. For example:

    ReadsExactly("the expected text")

The Resolution will then be passed in to an actor's test method, along
with a question to get the actual value. An assertion might look like:

    Perry.should_see_the(
        (Text.of(THE_WELCOME_MESSAGE), ReadsExactly("Welcome!")),
    )

Resolutions might be the only example of inheritance in the entirety of
ScreenPy. Hm.
"""


from hamcrest.core.base_matcher import BaseMatcher

from ..pacing import MINOR, beat


class Resolution(BaseMatcher):
    """
    An abstraction barrier for |PyHamcrest|'s matchers. Allows for
    more natural language possibilities as well as nice logging for the
    allure reports.

    You probably shouldn't expect to call any of the defined methods on
    this class or any inherited classes. Just pass an instantiated
    Resolution to your |Actor|, they'll know what to do with it.
    """

    @beat("... hoping {motivation}", gravitas=MINOR)
    def _matches(self, actual) -> bool:
        """passthrough to the matcher's method."""
        return self.matcher.matches(actual)

    @property
    def motivation(self) -> "Resolution":
        """Used to provide fancy logging for the allure report."""
        return self

    def __repr__(self) -> str:
        return self.line.format(expectation=self.expected)
