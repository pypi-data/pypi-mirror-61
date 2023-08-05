import json
import pathlib
import pydicom
import matplotlib
import matplotlib.pyplot as plt
import datetime
from dataclasses import dataclass
from typing import List, Optional, Dict, Any, Union, Tuple
from .events import Events
from .mark import Mark


@dataclass
class Image:
    """
    Container for a mammogram, stored in the DICOM_ format. An image can have
    zero or more marks for one or many lesions.

    :param id: SOP Instance UID, a unique identifier
    :param dcm_path: Path to the dicom image
    :param json_path: Path to the JSON file storing DICOM metadata
    :param marks: A list of marks or annotations, represented by
        :class:`omidb.mark.Mark`

    .. _DICOM: https://www.dicomstandard.org/
    """

    id: str
    dcm_path: pathlib.Path
    json_path: pathlib.Path
    marks: Optional[List[Mark]]
    _dcm: Optional[pydicom.FileDataset] = None
    _json: Optional[Dict[str, Any]] = None

    @property
    def dcm(self) -> pydicom.FileDataset:
        """
        Returns a :class:`pydicom.dataset.FileDataset`, representing a parsed DICOM file
        """

        if not self._dcm:
            self._dcm = pydicom.dcmread(str(self.dcm_path))

        return self._dcm

    def dcm_tags(self, tags: Union[str, List[str]]) -> pydicom.FileDataset:
        """
        Returns a pydicom.dataset.FileDataset, with only the specified tags of
        a parsed DICOM file and no pixel data
        """

        if isinstance(tags, str):
            tags = [tags]

        return pydicom.dcmread(str(self.dcm_path),
                               stop_before_pixels=True,
                               specific_tags=tags)

    @property
    def attributes(self) -> Optional[Dict[str, Any]]:
        """
        Access DICOM metadata via the JSON representation
        """

        if not self._json:
            with open(self.json_path) as f:
                self._json = json.load(f)

        return self._json

    def plot(
        self,
        ax: Optional[matplotlib.axes.Axes] = None
    ) -> matplotlib.image.AxesImage:
        """
        Plot the dicom
        """

        if not ax:
            fig, ax = plt.subplots()

        return ax.imshow(self.dcm.pixel_array, cmap=plt.cm.bone)
