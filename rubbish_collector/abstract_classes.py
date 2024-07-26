from abc import ABC, abstractmethod

class AbstractGetExtension(ABC):
    @abstractmethod
    def get_extension(self):
        pass

class AbstractCreatePath(ABC):
    @abstractmethod
    def create_path(self):
        pass

class AbstractCopyFile(ABC):
    @abstractmethod
    def copy_file(self):
        pass

class AbstractThreadPools(ABC):
    @abstractmethod
    def thread_pool(self):
        pass
    @abstractmethod
    def copy_file_task(self, file_path):
        pass