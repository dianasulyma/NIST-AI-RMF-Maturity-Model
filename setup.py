from pathlib import Path
from setuptools import setup, find_packages
from typing import List


def get_requirements(file_path: str) -> List[str]:
    """
    Return a list of requirements from the given file.
    Removes '-e .' entries used for editable installs.
    """
    HYPHEN_E_DOT = "-e ."

    with open(file_path) as file_obj:
        requirements = file_obj.read().splitlines()
        requirements = [req.strip() for req in requirements if req and not req.startswith("#")]

        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)

    return requirements


README = Path(__file__).with_name("README.md").read_text(encoding="utf-8")

setup(
    name="nist-maturity-model-application",
    version="0.0.1",
    description="Maturity model utilities.",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Diana",
    author_email="diana.rogachova4@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt"),
    python_requires=">=3.12.7",
    include_package_data=True,
)