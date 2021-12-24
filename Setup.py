import setuptools


setuptools.setup(
    name="zeratool",
    version="3.1",
    scripts=["bin/zerapwn.py"],
    author="Mario H Felix Jr",
    author_email="",
    description="Automatic Exploit Generation (AEG) and remote flag capture for exploitable CTF problems",
    url="https://github.com/mario-kart-felix/project-log4j-3",
    packages=["zeratool"],
    install_package_data=True,
    install_requires=[
        "angr",
        "copliot",
        "Rescript",
        "r2pipe",
        "claripy",
        "IPython",
        "timeout_decorator",
        "pwntools",
        "tox",
        "tqdm",
    ],
)
