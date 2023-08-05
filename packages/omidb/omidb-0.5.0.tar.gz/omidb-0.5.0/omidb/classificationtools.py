from .client import Client, Classification
from .episode import Episode
from .events import Event, SideOpinion
import copy
from typing import List

def episode_is_malignant(episode: Episode) -> bool:
    """
    Returns ``True`` if ``episode`` contains either a
    ``episode.events.surgery`` or ``episode.events.biopsy_wide`` event where
    the left or right opinion is malignant (``omidb.events.SideOpinion.OM``).

    :param episode: The episode to evaluate
    """

    try:

        surgery = episode.events.surgery
        return (
            surgery.left_opinion == SideOpinion.OM or  # type: ignore
            surgery.right_opinion == SideOpinion.OM  # type: ignore
        )
    except AttributeError as e:
        pass

    try: # What about biopsy fine?
        biopsy = episode.events.biopsy_wide
        return (
            biopsy.left_opinion == SideOpinion.OM or  # type: ignore
            biopsy.right_opinion == SideOpinion.OM  # type: ignore
        )
    except AttributeError:
        pass

    return False


def has_prior(client: Client) -> bool:
    """
    Returns ``True`` if ``client`` has a non-malignant episode earlier than a
    malignant episode; ``False`` otherwise.

    :param client: A classified client with more than one episode
    """

    if client.classification != Classification.M:
        return False

    nm_date = None  # earliest non-malignant date
    m_date = None  # most recent malignant date

    for episode in client.episodes:
        if None in (episode.id, episode.opened_date):
            continue

        date = episode.opened_date

        if episode_is_malignant(episode):
            if (m_date is None) or (date > m_date):
                m_date = date
        else:
            if (nm_date is None) or (date < nm_date):
                nm_date = date

        if nm_date and m_date:
            if nm_date < m_date:
                return True

    return False


def filter_studies_by_event_type(
    client: Client,
    event_type: List[Event],
    exact_match: bool = True
) -> Client:
    """
    Remove studies (``omidb.study.Study``) from ``client`` whose event type
    includes one or all (if ``exact_match`` is ``True``) of those listed by
    ``event_type``.

    :param client: A classified client with more than one episode
    :param event_type: A list of event types
    :param exact_match: If ``True`` the event types of a study must all of
        those in ``event_type``.
    """

    client2 = copy.deepcopy(client)

    for idx, episode in enumerate(client.episodes):
        for study in episode.studies:
            if study.event_type:
                if exact_match and set(study.event_type) != set(event_type):
                    client2.episodes[idx].studies.remove(study)
                elif not any([_ in study.event_type for _ in event_type]):
                    client2.episodes[idx].studies.remove(study)

    return client2
