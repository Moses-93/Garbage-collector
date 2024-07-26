```mermaid
classDiagram
    class RubbishCollectorSystem {
        + main()
    }

    class AbstractCreatePath {
        + create_path(): Path
    }

    class AbstractGetExtension {
        + get_extension(): str
    }

    class AbstractCopyFile {
        + copy_file()
    }

    class AbstractThreadPools {
        + thread_pool()
    }

    class GetExtension {
        - file_path: Path
        + get_extension(): str
        + __str__(): str
    }

    class CreatePath {
        - file_path: Path
        - target_dir: Path
        - extension: GetExtension
        + create_path(): Path
    }

    class CopyFile {
        - file_path: Path
        - create_path: CreatePath
        - target_path: Path
        + copy_file()
    }

    class ThreadPools {
        - file_paths: List[Path]
        - target_dir: Path
        - num_threads_used: int
        + thread_pool()
        + copy_file_task(file_path: Path)
    }

    RubbishCollectorSystem --> main
    GetExtension --|> AbstractGetExtension
    CreatePath --|> AbstractCreatePath
    CopyFile --|> AbstractCopyFile
    ThreadPools --|> AbstractThreadPools
    CreatePath "1" *-- "1" GetExtension
    CopyFile "1" *-- "1" CreatePath
    ThreadPools "1" *-- "n" CopyFile