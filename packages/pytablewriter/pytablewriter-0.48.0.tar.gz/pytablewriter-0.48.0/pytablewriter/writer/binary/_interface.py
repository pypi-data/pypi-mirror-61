import abc

from .._table_writer import AbstractTableWriter


class BinaryWriterInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def is_opened(self):  # pragma: no cover
        pass

    @abc.abstractmethod
    def open(self, file_path):  # pragma: no cover
        pass


class AbstractBinaryTableWriter(AbstractTableWriter, BinaryWriterInterface):
    @property
    def stream(self):
        return self._stream

    @stream.setter
    def stream(self, value):
        raise RuntimeError(
            "cannot assign a stream to binary format writers. use open method instead."
        )

    def __init__(self):
        super().__init__()

        self._stream = None

    def dumps(self):
        raise NotImplementedError("binary format writers did not support dumps method")

    def _verify_stream(self):
        if self.stream is None:
            raise OSError("null output stream. required to open(file_path) first.")
