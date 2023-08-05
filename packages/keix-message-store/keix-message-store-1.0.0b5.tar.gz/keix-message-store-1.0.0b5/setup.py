from setuptools import setup, find_packages
setup(
    name="keix-message-store",
    version="1.0.0-beta5",
    packages=find_packages(),
    author="Keix",
    python_requires='>3.5.2',
    author_email="info@keix.com",
    description="A gRPC client library for the Keix Message Store.",
    install_requires=[
        'grpcio==1.26.0',
        'msgpack==0.6.2'
    ]
)
