from typing import List, Iterable, Tuple, Union, Any, no_type_check, Optional, Iterator
from collections import namedtuple
import click
import csv
from ..client import Client
from ..image import Image
from ..study import Study
from ..series import Series
from ..episode import Episode
from ..parser import DB
from loguru import logger


def flatten(clients: Iterable[Client]) -> Iterator[
        Tuple[Client,
              Episode,
              Study,
              Series,
              Image]]:
    for client in clients:
        for episode in client.episodes:
            for study in episode.studies:
                for series in study.series:
                    for image in series.images:
                        yield(client, episode, study, series, image)


DicomAttributes = namedtuple(
    'DicomAttributes',
    'Manufacturer PresentationIntentType ImageLaterality ViewPosition ViewModCodeValue ViewModCodeMeaning'
)


@no_type_check
def extract_dicom_attributes(image: Image) -> DicomAttributes:
    """ Forcefully extract dicom attributes """
    try:
        manufacturer = image.attributes['00080070']['Value'][0]
    except:
        manufacturer = None

    try:
        presentation_intent_type = image.attributes['00080068']['Value'][0]
    except:
        presentation_intent_type = None

    try:
        image_laterality = image.attributes['00200062']['Value'][0]
    except:
        image_laterality = None

    try:
        view_position = image.attributes['00185101']['Value'][0]
    except:
        view_position = None

    try:
        view_mod_code_value = (
            image.attributes['00540220']['Value'][0]
            ['00080100']['Value'][0]
        )
    except:
        view_mod_code_value = None

    try:
        view_mod_code_meaning = (
            image.attributes['00540220']['Value'][0]
            ['00080104']['Value'][0]
        )
    except:
        view_mod_code_meaning = None

    return DicomAttributes(
        manufacturer,
        presentation_intent_type,
        image_laterality,
        view_position,
        view_mod_code_value,
        view_mod_code_meaning
    )


class DataWriter:
    def __init__(self) -> None:

        # Set up header
        self.rows: List[List[Any]] = [[
            'ClientID',
            'ClientClassification',
            'Site',
            'EpisodeID',
            'EpisodeType',
            'EpisodeAction',
            'EpisodeOpenedDate',
            'EpisodeClosedDate',
            'StudyInstanceUID',
            'StudyDate',
            'EventType',
            'SeriesInstanceUID',
            'SOPInstanceUID',
            'NumberOfMarks',
        ]]

        self.rows[0] += list(DicomAttributes._fields)

    def add(self,
            client: Client,
            episode: Episode,
            study: Study,
            series: Series,
            image: Image) -> None:

        tags = extract_dicom_attributes(image)

        event_types: List[Union[None, enums.Event]] = [None]

        if study.event_type:
            event_types = [e.name for e in study.event_type]

        num_marks: int = len(image.marks) if image.marks else 0

        # 1 row per event
        for event_type in event_types:

            ep_action = episode.action.name if episode.action else None
            ep_type = episode.type.name if episode.type else None

            self.rows.append(
                [
                    client.id,
                    client.classification.name,
                    client.site.name,
                    episode.id,
                    ep_type,
                    ep_action,
                    episode.opened_date,
                    episode.closed_date,
                    study.id,
                    study.date,
                    event_type,
                    series.id,
                    image.id,
                    num_marks,
                    *tags,
                ]
            )

    def write(self, outfile: str) -> None:
        with open(outfile, 'w') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerows(self.rows)


def run(db_path: str,
        outfile: str,
        clients: Optional[str] = None) -> None:

    client_list = None
    if clients:
        with open(clients, 'r') as f:
            client_list = [_.strip() for _ in f.readlines()]

    db = DB(db_path, clients=client_list)
    writer = write_client_data(db)
    writer.write(outfile)


def write_client_data(
    clients: Iterable[Client],
) -> DataWriter:
    writer: DataWriter = DataWriter()
    for client, episode, study, series, image in flatten(clients):
        writer.add(client, episode, study, series, image)
    return writer


@click.command('summarise')
@click.argument('db', type=click.Path(exists=True))
@click.argument('output-file', type=click.Path(exists=False))
@click.option(
    '--clients-file',
    type=click.Path(exists=True),
    help='File containing a list of clients to parse'
)
@click.option(
    '--log-file',
    type=click.Path(exists=False),
    help='Log to this file'
)
def cli(db: str, output_file: str, clients_file: str, log_file: str) -> None:
    """"Write a csv file, OUTPUT_FILE, summarising the content of OMI-DB,
    located at DB
    """

    logger.enable('omidb')

    if log_file:
        logger.remove()
        logger.add(log_file)

    run(db, output_file, clients_file)
