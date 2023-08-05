import datetime
import dataclasses
import re
import pathlib
import json
from typing import (List,
                    Dict,
                    Optional,
                    Iterator,
                    Any,
                    Sequence,
                    Union)
from loguru import logger
from . import utilities
from .client import Client, Classification, Site
from .episode import Episode
from . import episode
from .study import Study
from .series import Series
from .image import Image
from .mark import (
    BenignClassification,
    Conspicuity,
    MassClassification,
    BoundingBox,
    Mark
)

from .events import (
    Event,
    Events,
    BreastScreeningData,
    Screening,
    BaseEvent,
    Opinion,
    SideOpinion
)


class DB():
    """
    OMI-DB parser

    :param root_dir: Root directory of the OMI-DB. The `data` and `images`
        directories should sit somewhere below the root, and can be nested under
        sub-directories, e.g. ``data/sample/omi-db/(data|images)`` is fine.
    :param ignore_missing_images: If ``True``, the existence of dicom images
        belonging to a series will not be checked: parsing is based entirely on the
        JSON representations of the DICOM headers. Set to ``False`` to parse only
        those images for which you have *both* JSON and DICOM files for.
    :param clients: Only parse these clients, if they exist
    :param exclude_clients: Exclude these clients, even if they are in ``clients``
    """

    def __init__(self,
                 root_dir: Union[str, pathlib.Path],
                 ignore_missing_images: bool = True,
                 clients: Optional[Sequence[str]] = None,
                 exclude_clients: Optional[Sequence[str]] = None
                 ):

        root_dir = pathlib.Path(root_dir)
        self.ignore_missing_images = ignore_missing_images

        # The parent of the DATA/IMAGES directory
        self.real_root_dir = pathlib.Path()

        match = None
        for dir in root_dir.glob('**/'):
            match = re.match(r"(.*)/(data|images)", str(dir), re.I)
            if match:
                self.real_root_dir = pathlib.Path(match.group(1))
                break

        if match is None:
            raise ValueError('Failed to parse the given directory')

        if not clients:

            path_clients = (
                list(self.real_root_dir.glob('data/*')) +
                list(self.real_root_dir.glob('DATA/*'))
            )

            clients = [_.name for _ in path_clients]

        self.clients = set(clients)

        if exclude_clients:
            self.clients = set(clients) - set(exclude_clients)

    def __iter__(self) -> Iterator[Client]:
        """
        Iterates over all parsable clients found in the OMI-DB directory.

        :return: client_it: A :class:`omidb.client.Client` iterator
        """
        for client in self.clients:
            _data_dir = self._data_dir(client)
            studies: List[str] = []
            for study in _data_dir.glob('*/**'):

                # Extract study ID from path
                match = re.search(r"(\w+\d+)/(.*)", str(study))
                if match:
                    studies.append(match.group(2))

            try:
                episodes = self._episodes_from_imagedb(client, studies)

                classification: Classification = utilities.enum_lookup(  # type: ignore
                    self._nbss(client)['Classification'],
                    Classification
                )

                site: Site = utilities.enum_lookup(  # type: ignore
                    self._imagedb(client)['Site'],
                    Site
                )

                yield Client(
                    id=client,
                    episodes=episodes,
                    classification=classification,
                    site=site,
                )

            except Exception as e:
                logger.exception(
                    f'omidb: Failed to parse {client}, '
                )
                continue

    def _data_dir(self, client_id: str) -> pathlib.Path:
        """
        Path of the data directory corresponding to the client with ID
        `client_id`
        """
        p1 = self.real_root_dir / 'data' / client_id

        if p1.exists():
            return p1
        else:
            return self.real_root_dir / 'DATA' / client_id

    def _image_dir(self, client_id: str) -> pathlib.Path:
        """Path of the image directory corresponding to the client with ID
        `client_id`
        """
        p1 = self.real_root_dir / 'images' / client_id

        if p1.exists():
            return p1
        else:
            return self.real_root_dir / 'IMAGES' / client_id

    def _nbss_path(self, client_id: str) -> pathlib.Path:
        """Path of the NBSS json file corresponding to the client with ID
        `client_id`
        """

        p1 = self._data_dir(client_id) / ('nbss_' + client_id + '.json')

        if not p1.exists():
            p1 = self._data_dir(client_id) / ('NBSS_' + client_id + '.json')

        return p1

    def _nbss(self, client_id: str) -> Dict[str, Any]:
        """NBSS data corresponding to the client with ID `client_id`"""

        with open(self._nbss_path(client_id)) as f:
            nbss: Dict[str, Any] = json.load(f)
        return nbss

    def _imagedb(self, client_id: str) -> Dict[str, Any]:
        """IMAGEDB data corresponding to the client with ID `client_id`"""

        p1 = self._data_dir(client_id) / ('imagedb_' + client_id + '.json')

        if not p1.exists():
            p1 = self._data_dir(client_id) / ('IMAGEDB_' + client_id + '.json')

        with open(p1) as f:
            imagedb: Dict[str, Any] = json.load(f)

        return imagedb

    def _has_studies(self, client_id: str) -> bool:
        imagedb = self._imagedb(client_id)

        if (
            ('STUDIES' not in imagedb) or
            (not isinstance(imagedb['STUDIES'], dict))
        ):
            logger.error(
                f'No studies listed in IMAGEDB for client {client_id}'
            )

            return False

        return True

    def _parse_mark(self, mark_data: Dict[str, Any]) -> Mark:

        args: Dict[str, Any] = {}
        for param_name, key in zip((
            'architectural_distortion',
            'dystrophic_calcification',
            'fat_necrosis',
            'focal_asymmetry',
            'mass',
            'suspicious_calcifications',
            'milk_of_calcium',
            'other_benign_cluster',
            'plasma_cell_mastitis',
            'benign_skin_feature',
            'calcifications',
            'suture_calcification',
            'vascular_feature',
        ),
            (
            'ArchitecturalDistortion',
            'Dystrophic',
            'FatNecrosis',
            'FocalAsymmetry',
            'Mass',
            'SuspiciousCalcifications',
            'MilkOfCalcium',
            'OtherBenignCluster',
            'PlasmaCellMastitis',
            'Skin',
            'WithCalcification',
            'SutureCalcification',
            'Vascular',
        )):

            args[param_name] = True if mark_data.get(key) else None

        args['benign_classification'] = (
            utilities.enum_lookup(
                str(mark_data.get('BenignClassification')),
                BenignClassification
            )
        )

        args['conspicuity'] = utilities.enum_lookup(
            str(mark_data.get('Conspicuity')),
            Conspicuity
        )

        args['mass_classification'] = (
            utilities.enum_lookup(
                str(mark_data.get('MassClassification')),
                MassClassification
            )
        )

        args['lesion_id'] = str(mark_data['LinkedNBSSLesionNumber'])

        args['id'] = str(mark_data['MarkID'])

        args['boundingBox'] = BoundingBox(
            x1=int(mark_data['X1']),
            y1=int(mark_data['Y1']),
            x2=int(mark_data['X2']),
            y2=int(mark_data['Y2']),
        )

        return Mark(**args)

    def _parse_series(self,
                      client_id: str,
                      study: str,
                      study_data: Dict[str, Any]) -> List[Series]:

        series_list = []
        for series, series_dic in study_data.items():

            if not isinstance(series_dic, dict):
                continue

            image_list = list(series_dic.keys())

            images = []
            for image in image_list:

                dcm_path = (
                    self._image_dir(client_id) /
                    study /
                    (image + '.dcm')
                )

                json_path = (
                    self._data_dir(client_id) /
                    study /
                    (image + '.json')
                )

                # Due to inconsistency in file naming
                if not json_path.exists():
                    json_path = pathlib.Path(
                        str(json_path).replace('.json', '.dcm.json')
                    )

                if not json_path.exists():
                    logger.error(
                        f'Image metadata {json_path} does not exist, skipping.'
                    )
                    continue

                # Skip this image if no dcm file
                if not self.ignore_missing_images:
                    if not dcm_path.is_file():
                        logger.error(
                            f'Image {dcm_path} of does not exist, skipping.'
                        )
                        continue

                marks: List[Mark] = []

                image_marks_data = series_dic.get(image)
                if isinstance(image_marks_data, dict):

                    for mark_id, mark_data in image_marks_data.items():
                        try:
                            marks.append(self._parse_mark(mark_data))
                        except:
                            logger.exception(
                                f"Failed to parse mark data of {client_id} "
                                f"{image}.dcm"
                            )
                            continue

                images.append(
                    Image(image,
                          dcm_path,
                          json_path,
                          marks
                          )
                )

            series_list.append(Series(id=series, images=images))

        return series_list

    def _parse_events(self, episode_data: Dict[str, Any]) -> Events:
        event_kwargs = {
            'screening': episode_data.get('SCREENING'),
            'assessment': episode_data.get('ASSESSMENT'),
            'biopsy_wide': episode_data.get('BIOPSYWIDE'),
            'biopsy_fine': episode_data.get('BIOPSYFINE'),
            'clinical': episode_data.get('CLINICAL'),
            'surgery': episode_data.get('SURGERY'),
        }

        for key, value in event_kwargs.items():

            if not value:
                continue

            if key == 'screening':
                event_kwargs['screening'] = self._parse_screening_event(
                    value
                )
            else:
                event_kwargs[key] = self._parse_base_event(
                    value
                )

        return Events(**event_kwargs)

    def _parse_base_event(self, data: Dict[str, Any]) -> BaseEvent:

        dates: List[datetime.date] = []

        for i, side in enumerate(['L', 'R']):

            side_data = data.get(side)

            if not side_data:
                continue

            for lesion_id, lesion in side_data.items():
                if lesion.get('DatePerformed'):
                    date = utilities.str_to_date(lesion['DatePerformed'])
                    if date not in dates:
                        dates.append(date)

        left_opinion: SideOpinion = utilities.enum_lookup(  # type: ignore
            str(data.get('left_opinion')),
            SideOpinion
        )

        right_opinion: SideOpinion = utilities.enum_lookup(  # type: ignore
            str(data.get('right_opinion')),
            SideOpinion
        )

        return BaseEvent(
            left_opinion=left_opinion,
            right_opinion=right_opinion,
            dates=dates,
        )

    def _parse_screening_event(self, data: Dict[str, Any]) -> Screening:

        breast_data: List[Optional[BreastScreeningData]] = [None, None]
        dates: List[datetime.date] = []

        for i, side in enumerate(['L', 'R']):

            side_data = data.get(side)

            if not side_data:
                continue

            date: Optional[datetime.date] = None
            if side_data.get('DateTaken'):
                date = utilities.str_to_date(side_data['DateTaken'])
                if date not in dates:
                    dates.append(date)

            opinion: Optional[Opinion] = utilities.enum_lookup(  # type: ignore
                side_data.get('Opinion'),
                Opinion
            )

            breast_data[i] = (
                BreastScreeningData(
                    date=date,
                    equipment_make_model=side_data.get('EquipmentMakeModel'),
                    opinion=opinion,
                )
            )

        left_opinion: Optional[SideOpinion] = utilities.enum_lookup(  # type: ignore
            str(data.get('left_opinion')),
            SideOpinion
        )

        right_opinion: Optional[SideOpinion] = utilities.enum_lookup(  # type: ignore
            str(data.get('right_opinion')),
            SideOpinion
        )

        return Screening(
            left_opinion=left_opinion,
            right_opinion=right_opinion,
            left=breast_data[0],
            right=breast_data[1],
            dates=dates,
        )

    def _episodes_from_imagedb(
        self,
        client_id: str,
        studies: Optional[List[str]]) -> List[Episode]:
        """The beast, the animal, the dark knight.

        Prepare and instantiate all objects required for this client and the
        associated studies. Models are generated for only those images that
        exist locally.

        Note studies that cannot be linked to an NBSS event will not be
        aggregated.
        """

        if not self._has_studies(client_id):
            return []

        nbss = self._nbss(client_id)
        imagedb = self._imagedb(client_id)

        # Events for each episode
        events: Dict[str, Events] = {}
        for episode_id, nbss_episode in nbss.items():
            if isinstance(nbss_episode, dict):
                events[episode_id] = self._parse_events(nbss_episode)

        studies = [] if studies is None else studies
        # Studies for each episode
        episodes: Dict[str, List[Study]] = {}
        for study_id, study_data in imagedb['STUDIES'].items():

            if study_id not in studies:  # These exist locally
                if not study_id:
                    logger.error(
                        f'Empty study listed in IMAGEDB for client '
                        f'{client_id}...skipping'
                    )

                else:

                    logger.error(
                        f'{client_id}/{study_id} directory does not exist '
                        'but listed in IMAGEDB...skipping'
                    )

                continue

            series_list = self._parse_series(client_id,
                                             study_id,
                                             study_data)

            study_date = (
                utilities.str_to_date(study_data['StudyDate'])
                if study_data.get('StudyDate') else None
            )

            if study_data is None:
                logger.warning(f'{client_id}/{study_id} has no study date')
            # Try to extract episode ID by study-date <->event-date
            elif (
                ('EpisodeID' not in study_data) or
                (not study_data['EpisodeID']) or
                (study_data['EpisodeID'] not in nbss)
            ):
                logger.warning(
                    f"Episode {study_data.get('EpisodeID')} not found in NBSS "
                    f"for {client_id}/{study_id}, "
                    f"attempting link via event dates"
                )

                for episode_id, episode_events in events.items():
                    for field in dataclasses.fields(episode_events):
                        event = getattr(episode_events, field.name)
                        if event and (study_date in event.dates):
                            study_data['EpisodeID'] = episode_id
                            logger.info(
                                f'Linked study {study_id} to episode '
                                f'{episode_id}'
                            )
                            break

            # If still not episode ID, skip
            if (
                ('EpisodeID' not in study_data) or
                (not study_data['EpisodeID'])
            ):

                logger.error(
                    f'EpisodeID not found for {client_id}/{study_id}, skipping'
                )

                continue

            # Report if there are no events match study date
            matched_events = []
            if (study_data['EpisodeID'] in events) or (not study_data['EpisodeID']):

                episode_events = events[study_data['EpisodeID']]

                for field in dataclasses.fields(episode_events):
                    event = getattr(episode_events, field.name)
                    if event and (study_date in event.dates):
                        matched_events.append(getattr(Event, field.name))

                if not matched_events:
                    logger.warning(
                        f"No events in episode "
                        f"{study_data['EpisodeID']} match study date of "
                        f"{client_id}/{study_id}"
                    )

            else:
                logger.warning(
                    f"Episode {study_data['EpisodeID']} has no events "
                    "(episode not found in NBSS)"
                )
                continue

            # Now add studies to the episode
            study = Study(
                id=study_id,
                series=series_list,
                date=study_date,
                event_type=matched_events)

            if study_data['EpisodeID'] not in episodes:
                episodes[study_data['EpisodeID']] = [study]
            else:
                episodes[study_data['EpisodeID']].append(study)

        # Complete episode
        out = []
        for episode_id, episode_studies in episodes.items():

            if (episode_id not in nbss) or (episode_id not in events):

                logger.error(
                    f'Episode "{episode_id}" for client {client_id} '
                    'does not exist in NBSS, or has no events?'
                    'This episode is listed in IMAGEDB...skipping'
                )

                continue

            nbss_episode = nbss[episode_id]
            is_closed = (
                True if nbss_episode.get('EpisodeIsClosed') == 'Y'
                else False
            )

            ep_type: Optional[episode.Type] = utilities.enum_lookup(  # type: ignore
                nbss_episode.get('EpisodeType'),
                episode.Type
            )

            ep_action: Optional[episode.Action] = utilities.enum_lookup(  # type: ignore
                nbss_episode.get('EpisodeAction'),
                episode.Action
            )

            out.append(
                Episode(
                    id=episode_id,
                    events=events[episode_id],
                    studies=episode_studies,
                    type=ep_type,
                    action=ep_action,
                    opened_date=nbss_episode.get('EpisodeOpenedDate'),
                    closed_date=nbss_episode.get('EpisodeClosedDate'),
                    is_closed=is_closed,
                )
            )

        return out
