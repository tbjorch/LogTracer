import pathlib
from setuptools import setup

package_root = pathlib.Path(__file__).parent
readme = (package_root / "README.md").read_text()
setup(
    name="LogTracer",
    version="0.1.0",
    description="Tracer util allowing masking of arguments in the log",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/tbjorch/LogTracer",
    author="Tobias Björch",
    packages=["logtracer"],
    include_package_data=True,
    exclude_package_data={
        "gitignore": ".gitignore",
        "req-dev.txt": "requirements-dev.txt"
    }
)
