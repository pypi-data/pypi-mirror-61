import setuptools

setuptools.setup(
    name="queue_utilities",
    version="0.0.1",
    author="Jacob Richter",
    author_email="jaycorichter@gmail.com",
    description="Micropython compatible producer/subscriber event bus system with optional threading.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jaycosaur/queue-utilities",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
