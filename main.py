import sys
from pathlib import Path
from rubbish_collector.implementation_of_classes import ThreadPools
import os

def main():
    """
    The main function for the rubbish collector system.

    It takes command-line arguments for the source directory and an optional target directory.
    It then copies all files from the source directory to the target directory using a thread pool.

    Parameters:
    - None. However, it expects command-line arguments for the source directory and an optional target directory.

    Returns:
    - None. However, it prints usage instructions and error messages
    """

    # Check if the source directory is provided as a command-line argument
    if len(sys.argv) < 2:
        print("Usage: python main.py <source_directory> [<target_directory>]")
        sys.exit(1)

    # Get the source directory from the command-line argument
    src_dir = Path(sys.argv[1])

    # Check if the source directory exists
    if not src_dir.is_dir():
        print(f"Source directory {src_dir} does not exist.")
        sys.exit(1)

    # Get the target directory from the command-line argument or use a default value
    tar_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("dist")

    # Create the target directory if it does not exist
    if not tar_dir.exists():
        tar_dir.mkdir(parents=True)

    # Get a list of all file paths in the source directory
    file_paths = [Path(root) / file for root, _, files in os.walk(src_dir) for file in files]

    # Create an instance of the ThreadPools class and start copying files using a thread pool
    process = ThreadPools(file_paths, tar_dir)
    process.thread_pool()

    # Print a success message
    print(f"Files copied to {tar_dir}")

# Run the main function if the script is executed directly
if __name__ == "__main__":
    main()