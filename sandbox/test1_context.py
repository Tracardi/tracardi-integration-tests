import asyncio
from uuid import uuid4

import pytest

from tracardi.domain.entity import Entity
from tracardi.domain.payload.tracker_payload import TrackerPayload
from tracardi.domain.profile import Profile
from tracardi.domain.session import Session
from tracardi.service.storage.factory import StorageFor


def test_suite():
    @pytest.mark.asyncio
    async def test_session_exists_profile_not_exists():
        non_existent_profile_id = str(uuid4())

        # Create Session
        session_id = str(uuid4())
        session = Session(id=session_id)
        await StorageFor(session).index().save()

        # Profile does not exist
        session.profile = Profile(id=non_existent_profile_id)

        # Session exists and has profile equal to some random profile that do not exists
        tracker_payload = TrackerPayload(
            session=Entity(id=session_id),
            profile=None,
            source=Entity(id="scope")
        )

        profile, session = await tracker_payload.get_profile_and_session()

        assert isinstance(profile, Profile)
        assert isinstance(session, Session)

        assert profile.id != non_existent_profile_id  # profile can not be generated from non existent profile_id
        assert session.id == session_id

        await StorageFor(session).index().delete()
        await StorageFor(profile).index().delete()

    @pytest.mark.asyncio
    async def test_session_exists_profile_exists_conflict():
        # Create Profile for Tracker
        tracker_profile = Profile.new()
        await StorageFor(tracker_profile).index().save()

        # Create Profile for Session
        session_profile = Profile.new()
        await StorageFor(session_profile).index().save()

        # Create Session
        session_id = str(uuid4())
        session = Session(id=session_id)
        session.profile = session_profile
        await StorageFor(session).index().save()

        tracker_payload = TrackerPayload(
            session=Entity(id=session.id),
            profile=Entity(id=tracker_profile.id),
            source=Entity(id="scope")
        )

        profile, session = await tracker_payload.get_profile_and_session()

        assert isinstance(profile, Profile)
        assert isinstance(session, Session)

        assert profile.id == session_profile.id  # profile id must be form session
        assert session.id == session_id

        # Remove
        await StorageFor(session).index().delete()
        await StorageFor(tracker_profile).index().delete()
        await StorageFor(session_profile).index().delete()

    @pytest.mark.asyncio
    async def test_session_exists_profile_exists():
        # Create Profile for Session
        new_profile = Profile.new()
        await StorageFor(new_profile).index().save()

        # Create Session
        session_id = str(uuid4())
        session = Session(id=session_id)
        session.profile = new_profile
        await StorageFor(session).index().save()

        tracker_payload = TrackerPayload(
            session=Entity(id=session.id),
            profile=new_profile,
            source=Entity(id="scope")
        )

        profile, session = await tracker_payload.get_profile_and_session()

        assert isinstance(profile, Profile)
        assert isinstance(session, Session)

        assert profile.id == new_profile.id  # profile id must be form session
        assert session.id == session_id

        # Remove
        await StorageFor(session).index().delete()
        await StorageFor(profile).index().delete()

    @pytest.mark.asyncio
    async def test_session_not_exists_profile_exists():
        # Session does not exist
        # Profile exists

        # Create Profile for Session
        profile_id = str(uuid4())
        profile = Profile(id=profile_id)
        await StorageFor(profile).index().save()

        # Create Session
        session_id = str(uuid4())
        session = Session(id=session_id)
        session.profile = profile

        tracker_payload = TrackerPayload(
            session=Entity(id=session.id),
            profile=Entity(id=profile.id),
            source=Entity(id="scope")
        )

        profile, session = await tracker_payload.get_profile_and_session()

        assert isinstance(profile, Profile)
        assert isinstance(session, Session)

        assert profile.id == profile_id
        assert session.id == session_id

        # Remove
        await StorageFor(session).index().delete()
        await StorageFor(profile).index().delete()

    @pytest.mark.asyncio
    async def test_session_not_exists_profile_not_exists():
        # Create Profile for Session
        profile_id = str(uuid4())
        profile = Profile(id=profile_id)

        # Create Session
        session_id = str(uuid4())
        session = Session(id=session_id)
        session.profile = profile

        tracker_payload = TrackerPayload(
            session=Entity(id=session.id),
            profile=Entity(id=profile.id),
            source=Entity(id="scope")
        )

        profile, session = await tracker_payload.get_profile_and_session()

        assert profile.id != profile_id  # Must generate new profile, this may be forged
        assert session.id == session_id

        # Remove
        await StorageFor(session).index().delete()
        await StorageFor(profile).index().delete()

    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_session_exists_profile_not_exists())
    loop.run_until_complete(test_session_exists_profile_exists_conflict())
    loop.run_until_complete(test_session_exists_profile_exists())
    loop.run_until_complete(test_session_not_exists_profile_exists())
    loop.run_until_complete(test_session_not_exists_profile_not_exists())
    loop.close()
