from .models_abstract import *
from .models_general import *

# PROJECT UTILS
from utils.generals import is_model_registered

__all__ = list()

# 0
if not is_model_registered('debate', 'Category'):
    class Category(AbstractCategory):
        class Meta(AbstractCategory.Meta):
            db_table = 'debate_category'

    __all__.append('Category')


# 1
if not is_model_registered('debate', 'Tag'):
    class Tag(AbstractTag):
        class Meta(AbstractTag.Meta):
            db_table = 'debate_tag'

    __all__.append('Tag')


# 2
if not is_model_registered('debate', 'Vote'):
    class Vote(AbstractVote):
        class Meta(AbstractVote.Meta):
            db_table = 'debate_vote'

    __all__.append('Vote')


# 3
if not is_model_registered('debate', 'Attachment'):
    class Attachment(AbstractAttachment):
        class Meta(AbstractAttachment.Meta):
            db_table = 'debate_attachment'

    __all__.append('Attachment')


# 4
if not is_model_registered('debate', 'Topic'):
    class Topic(AbstractTopic):
        class Meta(AbstractTopic.Meta):
            db_table = 'debate_topic'

    __all__.append('Topic')


# 5
if not is_model_registered('debate', 'Response'):
    class Response(AbstractResponse):
        class Meta(AbstractResponse.Meta):
            db_table = 'debate_response'

    __all__.append('Response')


# 6
if not is_model_registered('debate', 'Discussed'):
    class Discussed(AbstractDiscussed):
        class Meta(AbstractDiscussed.Meta):
            db_table = 'debate_discussed'

    __all__.append('Discussed')


# 7
if not is_model_registered('debate', 'AccessMember'):
    class AccessMember(AbstractAccessMember):
        class Meta(AbstractAccessMember.Meta):
            db_table = 'debate_access_member'

    __all__.append('AccessMember')


# 8
if not is_model_registered('debate', 'AccessGroup'):
    class AccessGroup(AbstractAccessGroup):
        class Meta(AbstractAccessGroup.Meta):
            db_table = 'debate_access_group'

    __all__.append('AccessGroup')
