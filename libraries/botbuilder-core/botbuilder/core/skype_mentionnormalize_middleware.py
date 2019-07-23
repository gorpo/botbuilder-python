# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import Awaitable, Callable;
from .middleware_set import Middleware
from .turn_context import TurnContext
from botbuilder.schema import Activity
from xml.etree import ElementTree as ET

class SkypeMentionNormalizeMiddleware(Middleware):
    """SkypeMentionNormalizeMiddleware
    Middleware to patch mention Entities from Skype since they don't conform to expected values.
    
    Bots that interact with Skype should use this middleware if mentions are used.
 
    A Skype mention "text" field is of the format:
        <at id="28:2bc5b54d-5d48-4ff1-bd25-03dcbb5ce918">botname</at>
    But Activity.Text doesn't contain those tags and RemoveMentionText can't remove
    the entity from Activity.Text.
    This will remove the <at> nodes, leaving just the name.    
    """

    def on_process_request(self, context: TurnContext, logic: Callable[[TurnContext], Awaitable]):
        normalize_skype_mentiontext(context.activity)
        logic()

    @staticmethod
    def normalize_skype_mentiontext(activity: Activity):
        if(activity.channel_id == "skype" and activity.type == "message"):
            for entity in activity.entities:
                if(entity.type == "mention"):
                    mentionNameMatch = ET.fromstring(entity.additional_properties['text']).text
                    if(mentionNameMatch):
                        entity.additional_properties['text'] = mentionNameMatch
                    

