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
        return f"pip install {' '.join(libraries)}"
    elif lang == SupportedLanguage.JAVA:
        return f"mvn install:install-file -Dfile={' '.join(libraries)}"
    elif lang == SupportedLanguage.JAVASCRIPT:
        return f"yarn add {' '.join(libraries)}"
    elif lang == SupportedLanguage.CPP:
        return f"apt-get install {' '.join(libraries)}"
    elif lang == SupportedLanguage.GO:
        return f"go get {' '.join(libraries)}"
    elif lang == SupportedLanguage.RUBY:
        return f"gem install {' '.join(libraries)}"
    else:
        raise ValueError(f"Language {lang} is not supported")


def get_code_file_extension(lang: str) -> str:
    """
    Get the file extension for the given language
    :param lang: Programming language
    :return: File extension
    """
    extensions = {
        SupportedLanguage.PYTHON: "py",
        SupportedLanguage.JAVA: "java",
        SupportedLanguage.JAVASCRIPT: "js",
        SupportedLanguage.CPP: "cpp",
        SupportedLanguage.GO: "go",
        SupportedLanguage.RUBY: "rb",
    }
    return extensions.get(lang, ValueError(f"Language {lang} is not supported"))


def get_code_execution_command(lang: str, code_file: str) -> str:
    """
    Get the command to execute the code
    :param lang: Programming language
    :param code_file: Path to the code file
    :return: Execution command
    """
    commands = {
        SupportedLanguage.PYTHON: f"python {code_file}",
        SupportedLanguage.JAVA: f"java {code_file}",
        SupportedLanguage.JAVASCRIPT: f"node {code_file}",
        SupportedLanguage.CPP: f"./{code_file}",
        SupportedLanguage.GO: f"go run {code_file}",
        SupportedLanguage.RUBY: f"ruby {code_file}",
    }
    return commands.get(lang, ValueError(f"Language {lang} is not supported"))