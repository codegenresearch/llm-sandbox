import docker
from typing import List, Optional
import os
from docker import DockerClient
from llm_sandbox.const import SupportedLanguage, DefaultImage, NotSupportedLibraryInstallation


def image_exists(client: DockerClient, image: str) -> bool:
    """
    Check if a Docker image exists.
    :param client: Docker client.
    :param image: Docker image name.
    :return: True if the image exists, False otherwise.
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
    Get the command to install libraries for the given language.
    :param lang: Programming language.
    :param libraries: List of libraries.
    :return: Installation command.
    """
    if lang == SupportedLanguage.PYTHON:
        return f"pip install {' '.join(libraries)}"
    elif lang == SupportedLanguage.JAVA:
        return f"mvn install:install-file -Dfile={' '.join(libraries)}"
    elif lang == SupportedLanguage.JAVASCRIPT:
        return f"yarn add {' '.join(libraries)}"
    elif lang == SupportedLanguage.CPP:
        return f"apt-get update && apt-get install -y {' '.join(libraries)}"
    elif lang == SupportedLanguage.GO:
        return f"go get {' '.join(libraries)}"
    elif lang == SupportedLanguage.RUBY:
        return f"gem install {' '.join(libraries)}"
    else:
        raise ValueError(f"Language {lang} is not supported")


def get_code_file_extension(lang: str) -> str:
    """
    Get the file extension for the given language.
    :param lang: Programming language.
    :return: File extension.
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
        raise ValueError(f"Language {lang} is not supported")


def get_code_execution_command(lang: str, code_file: str) -> List[str]:
    """
    Get the command to execute the code.
    :param lang: Programming language.
    :param code_file: Path to the code file.
    :return: List of execution commands.
    """
    if lang == SupportedLanguage.PYTHON:
        return [f"python {code_file}"]
    elif lang == SupportedLanguage.JAVA:
        class_name = code_file.split('.')[0]
        return [f"javac {code_file}", f"java {class_name}"]
    elif lang == SupportedLanguage.JAVASCRIPT:
        return [f"node {code_file}"]
    elif lang == SupportedLanguage.CPP:
        return [f"g++ {code_file} -o a.out", f"./a.out"]
    elif lang == SupportedLanguage.GO:
        return [f"go run {code_file}"]
    elif lang == SupportedLanguage.RUBY:
        return [f"ruby {code_file}"]
    else:
        raise ValueError(f"Language {lang} is not supported")


def run_code_in_docker(lang: str, code: str, libraries: List[str] = None):
    client = docker.from_env()
    image = DefaultImage.__dict__.get(lang.upper())
    if not image:
        raise ValueError(f"Default image for language {lang} is not defined")

    if not image_exists(client, image):
        print(f"Pulling image {image}...")
        client.images.pull(image)

    code_file_extension = get_code_file_extension(lang)
    code_file_name = f"code.{code_file_extension}"
    code_file_path = f"/sandbox/{code_file_name}"

    commands = []
    if libraries and lang not in NotSupportedLibraryInstallation:
        install_command = get_libraries_installation_command(lang, libraries)
        commands.append(install_command)

    commands.append(f"echo '{code}' > {code_file_path}")
    commands.extend(get_code_execution_command(lang, code_file_name))

    command = " && ".join(commands)

    container = client.containers.run(
        image,
        command,
        volumes={os.getcwd(): {'bind': '/sandbox', 'mode': 'rw'}},
        remove=True,
        stdout=True,
        stderr=True,
        detach=False
    )

    output = container.decode('utf-8')
    print(output)


if __name__ == "__main__":
    run_code_in_docker("python", "print('Hello, World!')")
    run_code_in_docker("java", """
    public class Main {
        public static void main(String[] args) {
            System.out.println("Hello, World!");
        }
    }
    """)
    run_code_in_docker("javascript", "console.log('Hello, World!')")
    run_code_in_docker("cpp", """
    #include <iostream>
    int main() {
        std::cout << "Hello, World!" << std::endl;
        return 0;
    }
    """)
    run_code_in_docker("go", """
    package main
    import "fmt"
    func main() {
        fmt.Println("Hello, World!")
    }
    """)
    run_code_in_docker("ruby", "puts 'Hello, World!'")