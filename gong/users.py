from dataclasses import dataclass
from typing import List

from gong.base import GongHTTPObjectBase, GongRecords


@dataclass
class GongUserSettings(GongHTTPObjectBase):
    emails_imported: bool
    gong_connect_enabled: bool
    non_recorded_meetings_imported: bool
    prevent_email_import: bool
    prevent_web_conference_recording: bool
    telephony_calls_imported: bool
    web_conferences_recorded: bool


@dataclass
class GongUserSpokenLanguage(GongHTTPObjectBase):
    language: str
    primary: bool


@dataclass
class GongUser(GongHTTPObjectBase):
    id: str
    active: bool
    created: str
    email_address: str
    extension: str
    first_name: str
    last_name: str
    manager_id: str
    meeting_consent_page_url: str
    phone_number: str
    settings: GongUserSettings
    title: str
    trusted_email_address: str
    email_aliases: List[str] = None
    personal_meeting_urls: List[str] = None
    spoken_languages : List[GongUserSpokenLanguage] = None


@dataclass
class GongUserResponse(GongHTTPObjectBase):
    request_id: str
    user: GongUser


@dataclass
class GongUsersResponse(GongHTTPObjectBase):
    request_id: str
    records: GongRecords
    users: List[GongUser]