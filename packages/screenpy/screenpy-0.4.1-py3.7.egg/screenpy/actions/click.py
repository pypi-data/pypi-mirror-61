"""
An action to click on an element. An actor must possess the ability to
BrowseTheWeb to perform this action. An actor performs this action like
so:

    the_actor.attempts_to(Click.on_the(LOGIN_LINK))

    the_actor.attempts_to(
        Click.on(THE_MODAL_LAUNCHER).then_wait_for_the(MODAL)
    )
"""


import warnings
from typing import Union

from ..actor import Actor
from ..pacing import MINOR, beat
from ..target import Target
from .base_action import Action
from .wait import Wait


class Click(Action):
    """
    Clicks on an element! A Click action is expected to be instantiated
    via its static |Click.on| or |Click.on_the| methods. A typical
    invocation might look like:

        Click.on_the(PROFILE_LINK).then_wait_for(ACCOUNT_WELCOME_MESSAGE)

    It can then be passed along to the |Actor| to perform the action.
    """

    target: Target
    action_complete_target: Union[None, Target]

    @staticmethod
    def on_the(target: Target) -> "Click":
        """
        Creates a new Click action with its crosshairs aimed at the
        provided target.

        Args:
            target: The |Target| describing the element to click.

        Returns:
            |Click|
        """
        return Click(target)

    @staticmethod
    def on(target: Target) -> "Click":
        """Syntactic sugar for |Click.on_the|."""
        return Click.on(target)

    def then_wait_for_the(self, target: Target) -> "Click":
        """
        Supplies a target to wait for after performing the click.

        Args:
            target: The |Target| describing the element to wait for after
                performing the click.

        Returns:
            |Click|
        """
        warnings.warn(
            "Click.then_wait_for_the is deprecated. Please use the new Wait action "
            "instead.",
            DeprecationWarning,
        )

        self.action_complete_target = target
        return self

    def then_wait_for(self, target: Target) -> "Click":
        """Syntactic sugar for |Click.then_wait_for_the|."""
        return self.then_wait_for(target)

    @beat("{0} clicks on the {target}.", gravitas=MINOR)
    def perform_as(self, the_actor: Actor) -> None:
        """
        Asks the actor to find the element described by the stored target,
        and then clicks it. May wait for another target to appear, if
        |Click.then_wait_for| had been called.

        Args:
            the_actor: the |Actor| who will perform the action.

        Raises:
            |UnableToPerformException|: if the actor does not have the
                ability to |BrowseTheWeb|.
        """
        element = self.target.found_by(the_actor)
        element.click()
        if self.action_complete_target is not None:
            the_actor.attempts_to(Wait.for_the(self.action_complete_target).to_appear())

    def __init__(self, target: Target) -> None:
        self.target = target
        self.action_complete_target = None
