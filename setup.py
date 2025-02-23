from setuptools import setup

setup(name='cbpi4_AJ_SR04M',
      version='0.0.1',
      description='CraftBeerPi Plugin for Ultrasonic Distance Sensor AJ-SR04M',
      author='Kenny',
      author_email='',
      url='',
      include_package_data=True,
      package_data={
        # If any package contains *.txt or *.rst files, include them:
      '': ['*.txt', '*.rst', '*.yaml'],
      'cbpi4_AJ_SR04M': ['*','*.txt', '*.rst', '*.yaml']},
      packages=['cbpi4_AJ_SR04M'],
     )
