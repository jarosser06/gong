from dataclasses import asdict, dataclass
from datetime import datetime
from typing import List, Optional, Union

from gong.base import GongHTTPObjectBase, GongRecords


@dataclass
class GongCallBaseFilter(GongHTTPObjectBase):
    '''
    GongCallBaseFilter is a dataclass that represents the base filter for the Gong Call API.

    Args:
        call_ids (Optional[List[str]]): List of call IDs.
        from_date_time (Optional[Union[datetime, int]]): From date time.
        primary_user_ids (Optional[List[str]]): List of primary user IDs.
        to_date_time (Optional[Union[datetime, int]]): To date time.
        workspace_id (Optional[str]): Workspace ID
    '''
    call_ids: Optional[List[str]] = None
    from_date_time: Optional[Union[datetime, int]] = None
    primary_user_ids: Optional[List[str]] = None
    to_date_time: Optional[Union[datetime, int]] = None
    workspace_id: Optional[str] = None

    def __post_init__(self):
        super().__post_init__()

        if isinstance(self.from_date_time, int):
            self.from_date_time = datetime.fromtimestamp(self.from_date_time)
        elif isinstance(self.from_date_time, datetime):
            self.from_date_time = self.from_date_time.isoformat(timespec='seconds')

        if isinstance(self.to_date_time, int):
            self.to_date_time = datetime.fromtimestamp(self.to_date_time)
        elif isinstance(self.to_date_time, datetime):
            self.to_date_time = self.to_date_time.isoformat(timespec='seconds')


@dataclass
class GongCallExposedFieldsContent(GongHTTPObjectBase):
    structure: bool = None
    topics: bool = None
    trackers: bool = None
    tracker_occurences: bool = None
    points_of_interest: bool = None
    brief: bool = None
    outline: bool = None
    highlights: bool = None
    call_outcome: bool = None
    key_points: bool = None


@dataclass
class GongCallExposedFieldsInteraction(GongHTTPObjectBase):
    speakers: bool = None
    video: bool = None
    person_interaction_stats: bool = None
    questions: bool = None


@dataclass
class GongCallExposedFieldsCollaboration(GongHTTPObjectBase):
    public_comments: bool = None


@dataclass
class GongCallExposedFields(GongHTTPObjectBase):
    parties: bool = None
    content: GongCallExposedFieldsContent = None
    interaction: GongCallExposedFieldsInteraction = None
    collaboration: GongCallExposedFieldsCollaboration = None
    media: bool = None


@dataclass
class GongCallContentSelector(GongHTTPObjectBase):
    context: str = None
    context_timing: str = None
    exposed_fields: GongCallExposedFields = None


@dataclass
class GongCallTranscriptFilter(GongHTTPObjectBase):
    cursor: Optional[str] = None
    filter: Optional[GongCallBaseFilter] = None


@dataclass
class GongCallDetailsFilter(GongHTTPObjectBase):
    cursor: Optional[str] = None
    filter: Optional[GongCallBaseFilter] = None
    content_selector: Optional[GongCallContentSelector] = None


@dataclass
class GongCall(GongHTTPObjectBase):
    calendar_event_id: str
    id: str
    client_unique_id: str
    direction: str
    duration: int
    is_private: bool
    language: str
    media: str
    meeting_url: str
    primary_user_id: str
    purpose: str
    scheduled: Union[datetime, int]
    scope: str
    sdr_disposition: str
    started: Union[datetime, int]
    system: str
    title: str
    url: str
    workspace_id: str
    custom_data: Optional[str] = None

    def __post_init__(self):
        if isinstance(self.scheduled, int):
            self.scheduled = datetime.fromtimestamp(self.scheduled)
        elif isinstance(self.scheduled, str):
            self.scheduled = datetime.fromisoformat(self.scheduled)

        if isinstance(self.started, int):
            self.started = datetime.fromtimestamp(self.started)
        elif isinstance(self.started, str):
            self.started = datetime.fromisoformat(self.started)

    def to_dict(self):
        return asdict(self)


@dataclass
class GongCallContextObjectField(GongHTTPObjectBase):
    name: str
    value: str


@dataclass
class GongCallContextObject(GongHTTPObjectBase):
    fields: List[GongCallContextObjectField]
    object_type: str
    object_id: str
    timing: str


@dataclass
class GongCallContext(GongHTTPObjectBase):
    system: str


@dataclass
class GongCallParty(GongHTTPObjectBase):
    id: str
    affiliation: str
    speaker_id: str
    context: List[GongCallContext] = None
    email_address: str = None
    methods: str = None
    name: str = None
    phone_number: str = None
    user_id: str = None
    title: str = None


@dataclass
class GongCallMonologueSentence(GongHTTPObjectBase):
    end: int
    start: int
    text: str


@dataclass
class GongCallMonologue(GongHTTPObjectBase):
    sentences: List[GongCallMonologueSentence]
    speaker_id: str
    topic: str


@dataclass
class GongCallTranscript(GongHTTPObjectBase):
    call_id: str
    transcript: List[GongCallMonologue]


@dataclass
class GongGetCallsResponse(GongHTTPObjectBase):
    calls: List[GongCall]
    records: GongRecords
    request_id: str


@dataclass
class GongCallDetailsCallItem(GongHTTPObjectBase):
    duration: int
    name: str


@dataclass
class GongCallDetailsCallOccurrence(GongHTTPObjectBase):
    start_time: float
    speaker_id: str


@dataclass
class GongCallDetailsCallPhrase(GongHTTPObjectBase):
    count: int
    occurences: List[GongCallDetailsCallOccurrence]
    phrase: str


@dataclass
class GongCallDetailsCallTracker(GongHTTPObjectBase):
    id: str
    name: str
    count: int
    type: str
    occurrences: List[GongCallDetailsCallOccurrence]
    phrases: List[GongCallDetailsCallPhrase]


@dataclass
class GongCallDetailsCallActionItem(GongHTTPObjectBase):
    snippet: str
    snippet_start_time: float
    snippet_end_time: float
    speaker_id: str


@dataclass
class GongCallDetailsCallPointsOfInterest(GongHTTPObjectBase):
    action_items: List[GongCallDetailsCallActionItem]


@dataclass
class GongCallDetailsCallOutlineItem(GongHTTPObjectBase):
    start_time: float
    text: str


@dataclass
class GongCallDetailsCallOutline(GongHTTPObjectBase):
    duration: float
    items: List[GongCallDetailsCallOutlineItem]
    start_time: float
    section: str


@dataclass
class GongCallDetailsCallHighlightItem(GongHTTPObjectBase):
    start_times: List[float]
    text: str


@dataclass
class GongCallDetailsCallHighlight(GongHTTPObjectBase):
    title: str
    items: List[GongCallDetailsCallHighlightItem]


@dataclass
class GongCallDetailsCallOutcome(GongHTTPObjectBase):
    id: str
    category: str
    name: str


@dataclass
class GongCallDetailsCallKeyPoint(GongHTTPObjectBase):
    text: str


@dataclass
class GongCallDetailsContent(GongHTTPObjectBase):
    brief: str
    call_outcome: GongCallDetailsCallOutcome
    highlights: List[GongCallDetailsCallHighlight]
    key_points: List[GongCallDetailsCallKeyPoint]
    outline: List[GongCallDetailsCallOutline]
    points_of_interest: GongCallDetailsCallPointsOfInterest
    structure: List[GongCallDetailsCallItem]
    topics: List[GongCallDetailsCallItem]
    trackers: List[GongCallDetailsCallTracker]


@dataclass
class GongCallDetailsInterationSpeaker(GongHTTPObjectBase):
    id: str
    talk_time: str
    user_id: str


@dataclass
class GongCallDetailsInteractionStat(GongHTTPObjectBase):
    name: str
    value: int


@dataclass
class GongCallDetailsInteractionVideo(GongHTTPObjectBase):
    name: str
    duration: float


@dataclass
class GongCallDetailsInteractionQuestions(GongHTTPObjectBase):
    company_count: int
    non_company_count: int


@dataclass
class GongCallDetailsInteraction(GongHTTPObjectBase):
    speakers: List[GongCallDetailsInterationSpeaker]
    interaction_stats: List[GongCallDetailsInteractionStat]
    video: List[GongCallDetailsInteractionVideo]
    questions: GongCallDetailsInteractionQuestions


@dataclass
class GongCallDetailsPublicComment(GongHTTPObjectBase):
    id: str
    audio_start_time: float
    audio_end_time: float
    commenter_user_id: str
    comment: str
    during_call: bool
    in_reply_to: str
    posted: datetime


@dataclass
class GongCallDetailsCollaboration(GongHTTPObjectBase):
    public_comments: List[GongCallDetailsPublicComment]


@dataclass
class GongCallDetailsMedia(GongHTTPObjectBase):
    audio: str
    video: str


@dataclass
class GongCallDetails(GongHTTPObjectBase):
    content: GongCallDetailsContent = None
    context: List[GongCallContextObject] = None
    meta_data: GongCall = None
    parties: List[GongCallParty] = None
    interaction: GongCallDetailsInteraction = None
    collaboration: GongCallDetailsCollaboration = None
    media: GongCallDetailsMedia = None


@dataclass
class GongCallDetailsRequest(GongHTTPObjectBase):
    cursor: str = None
    filter: GongCallBaseFilter = None
    content_selector: GongCallContentSelector = None


@dataclass
class GongGetCallDetailsResponse(GongHTTPObjectBase):
    calls: List[GongCallDetails]
    records: GongRecords
    request_id: str


@dataclass
class GongCallTranscriptResponse(GongHTTPObjectBase):
    call_transcripts: List[GongCallTranscript]
    records: GongRecords
    request_id: str