"""Provides the DicomImporter class."""

from ... import util
from ..template import create_scanner_node
from .abstract_importer import AbstractImporter


class DicomImporter(AbstractImporter):
    """Importer class to import DICOM files."""
    help_text = "Dicom importer"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.config.subject:
            util.set_nested_attr(self.context, "subject.label", self.config.subject)
        if self.config.session:
            util.set_nested_attr(self.context, "session.label", self.config.session)

    def initialize(self):
        """Initialize the importer."""
        self.add_template_node(create_scanner_node("dicom"))
