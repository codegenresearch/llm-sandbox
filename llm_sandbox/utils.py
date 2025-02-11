import docker
import docker.errors
from typing import List, Optional

from docker import DockerClient
from llm_sandbox.const import SupportedLanguage


def image_exists(client: DockerClient, image: str) -> bool:
    """
    Check if a Docker image exists
    :param client: Docker client
    :param image: Docker image
    :return: True if the image exists, False otherwise
    """
    try:
        client.images.get(image)
        return True
    except docker.errors.ImageNotFound:
        return False
    except Exception as e:
        raise e


def get_libraries_installation_command(lang: str, libraries: List[str]) -> Optional[str]:
    """
    Get the command to install libraries for the given language
    :param lang: Programming language
    :param libraries: List of libraries
    :return: Installation command
    """
    if lang == SupportedLanguage.PYTHON:
        return "pip install " + " ".join(libraries)
    elif lang == SupportedLanguage.JAVA:
        return "mvn install:install-file -Dfile=" + " ".join(libraries)
    elif lang == SupportedLanguage.JAVASCRIPT:
        return "yarn add " + " ".join(libraries)
    elif lang == SupportedLanguage.CPP:
        return "apt-get install " + " ".join(libraries)
    elif lang == SupportedLanguage.GO:
        return "go get " + " ".join(libraries)
    elif lang == SupportedLanguage.RUBY:
        return "gem install " + " ".join(libraries)
    else:
        raise ValueError("Language " + lang + " is not supported")


def get_code_file_extension(lang: str) -> str:
    """
    Get the file extension for the given language
    :param lang: Programming language
    :return: File extension
    """
    if lang == SupportedLanguage.PYTHON:
        return "py"
    elif lang == SupportedLanguage.JAVA:
        return "java"
    elif lang == SupportedLanguage.JAVASCRIPT:
        return "js"
    elif lang == SupportedLanguage.CPP:
        return "cpp"
    elif lang == SupportedLanguage.GO:
        return "go"
    elif lang == SupportedLanguage.RUBY:
        return "rb"
    else:
        raise ValueError("Language " + lang + " is not supported")


def get_code_execution_command(lang: str, code_file: str) -> list:
    """
    Get the commands to execute the code
    :param lang: Programming language
    :param code_file: Path to the code file
    :return: List of execution commands
    """
    if lang == SupportedLanguage.PYTHON:
        return ["python " + code_file]
    elif lang == SupportedLanguage.JAVA:
        class_name = code_file.split(".")[0]
        return ["javac " + code_file, "java " + class_name]
    elif lang == SupportedLanguage.JAVASCRIPT:
        return ["node " + code_file]
    elif lang == SupportedLanguage.CPP:
        return ["g++ -o a.out " + code_file, "./a.out"]
    elif lang == SupportedLanguage.GO:
        return ["go run " + code_file]
    elif lang == SupportedLanguage.RUBY:
        return ["ruby " + code_file]
    else:
        raise ValueError("Language " + lang + " is not supported")


def verify_directory_exists(client: DockerClient, container_id: str, directory: str) -> bool:
    """
    Verify if a directory exists in the container
    :param client: Docker client
    :param container_id: Container ID
    :param directory: Directory path to verify
    :return: True if the directory exists, False otherwise
    """
    try:
        exec_command = "test -d " + directory
        exec_id = client.containers.get(container_id).exec_run(exec_command)
        return exec_id.exit_code == 0
    except Exception as e:
        raise e