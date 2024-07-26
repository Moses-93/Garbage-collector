# Implementation of classes for a rubbish collector system

from rubbish_collector.abstract_classes import (AbstractCreatePath, 
                                               AbstractGetExtension, 
                                               AbstractCopyFile,
                                               AbstractThreadPools)
from pathlib import Path
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed


class GetExtension(AbstractGetExtension):
    """
    A class to get the extension of a file.

    Attributes:
    - file_path (Path): The Path object representing the file path.

    Methods:
    - get_extension(): Returns the extension of the file.
    - __str__(): Returns a string representation of the GetExtension object.
    """

    def __init__(self, file_path):
        if not isinstance(file_path, Path):
            raise ValueError("file_path must be a Path object")
        self.file_path = file_path

    def get_extension(self):
        self.extension = self.file_path.suffix[1:]
        return self.extension

    def __str__(self) -> str:
        return f"File extension: {self.extension}"


class CreatePath(AbstractCreatePath):
    """
    A class to create a target path for a file based on its extension.

    Attributes:
    - file_path (Path): The Path object representing the file path.
    - target_dir (Path): The Path object representing the target directory.
    - extension (GetExtension): An instance of the GetExtension class.

    Methods:
    - create_path(): Creates the target path based on the file extension and returns it.
    """

    def __init__(self, file_path, target_dir) -> None:
        self.file_path = file_path
        self.target_dir = target_dir
        self.extension = GetExtension(file_path)

    def create_path(self):
        ext = self.extension.get_extension()
        self.target_path = self.target_dir / ext / self.file_path.name
        self.target_path.parent.mkdir(parents=True, exist_ok=True)
        return self.target_path


class CopyFile(AbstractCopyFile):
    """
    A class to copy a file to a target directory.

    Attributes:
    - file_path (Path): The Path object representing the file path.
    - create_path (CreatePath): An instance of the CreatePath class.
    - target_path (Path): The Path object representing the target path.

    Methods:
    - copy_file(): Copies the file to the target directory.
    """

    def __init__(self, file_path, target_dir) -> None:
        self.file_path = file_path
        self.create_path = CreatePath(file_path, target_dir)
        self.target_path = self.create_path.create_path()

    def copy_file(self):
        shutil.copy2(self.file_path, self.target_path)


class ThreadPools(AbstractThreadPools):
    """
    A class to manage file copying using a thread pool.

    Attributes:
    - file_paths (List[Path]): A list of Path objects representing the file paths to be copied.
    - target_dir (Path): The Path object representing the target directory.
    - num_threads_used (int): The number of threads used for copying files.

    Methods:
    - thread_pool(): Uses a ThreadPoolExecutor to copy files from the file_paths list to the target directory.
    - copy_file_task(): A helper function to copy a single file using the CopyFile class.
    """

    def __init__(self, file_paths, target_dir) -> None:
        self.file_paths = file_paths
        self.target_dir = target_dir
        self.num_threads_used = 0

    def thread_pool(self):
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.copy_file_task, file_path) for file_path in self.file_paths]
            self.num_threads_used = len(futures)
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"Exception occurred: {e}")

        print(f"Number of threads used: {self.num_threads_used}")

    def copy_file_task(self, file_path):
        process = CopyFile(file_path, self.target_dir)
        process.copy_file()