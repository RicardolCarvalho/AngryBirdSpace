from setuptools import setup, find_packages

setup(
    name="angrybirdspace",
    version="0.1.0",
    author="Ricardo Luz Carvalho, Isabela Vieira Rodrigues",
    author_email="ricardolc2@al.insper.edu, isabelavr@al.insper.edu.br",
    description="Uma recriação do Angry Birds Space em Pygame.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/RicardolCarvalho/AngryBirdSpace.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',

    package_data={
        '', ['img/*.png', 'img/*.jpg', 'img/*.webp', 'angrybirdspace/img/*.png', 'angrybirdspace/img/*.jpg', 'angrybirdspace/img/*.webp']
    },

    entry_points={
        'console_scripts': [
            'angrybirdspace=angrybirdspace.main:main'
        ]
    },
    install_requires=[
        'pygame',
        'numpy'
    ]
)
