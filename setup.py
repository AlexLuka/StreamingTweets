from setuptools import setup, find_packages
import tw_streamer


setup(
    name='tw_streamer',
    version=tw_streamer.__version__,
    description='Test Project To Work With Tweeter Streaming API',
    author='alelu',
    author_email='nomail@nowhere.com',
    url='',
    packages=find_packages(),
    install_requires=[
        'matplotlib',
        'redis',
        'tweepy'
    ]
)