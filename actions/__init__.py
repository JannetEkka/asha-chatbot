"""
This file imports all actions to register them with the Rasa SDK.
"""

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, AllSlotsReset, UserUtteranceReverted

from .actions import ActionSearchJobs
from .actions import ActionProvideEventsInfo
from .actions import ActionProvideSessionsInfo
from .actions import ActionProvideMentorshipInfo
from .actions import ActionHandleFAQ
from .actions import ActionAddressGenderBias
from .actions import ActionPauseConversation
from .actions import ActionResumeConversation
from .actions import ValidateJobSearchForm
# Optional: If you implement the test handler as a separate class
# from .actions import ActionTestGeminiAPI