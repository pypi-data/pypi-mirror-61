from distutils.core import setup
setup(
  name = 'timecoach', # How you named your package folder (MyLib)
  packages = ['timecoach'], # Chose the same as "name"
  version = '0.1.1', # Start with a small number and increase it with every change you make
  license= 'MIT', # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'a utility library for generating chunks of time within a datetime range', # Give a short description about your library
  author = 'Jason Yung',
  author_email = 'json.yung@gmail.com',
  url = 'https://github.com/json2d/timecoach', # Provide either the link to your github or to your website
  download_url = 'https://github.com/json2d/timecoach/archive/v0.1.1.tar.gz',
  keywords = ['datetime', 'interval', 'chunks'], # Keywords that define your package best
  install_requires= [
    'python-dateutil',
  ],
  classifiers=[
    'Development Status :: 3 - Alpha', # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers', # Define your audience
    'Topic :: Utilities',
    'License :: OSI Approved :: MIT License', # Again, pick a license
    'Programming Language :: Python :: 3', # Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)