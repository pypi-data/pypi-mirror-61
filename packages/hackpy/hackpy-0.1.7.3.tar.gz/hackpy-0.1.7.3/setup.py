from setuptools import setup, find_packages

setup(name='hackpy',
      version='0.1.7.3',
      description='The project is no longer maintained.   Full description here: https://github.com/LimerBoy/hackpy/blob/master/README.MD',
      url='https://github.com/LimerBoy/hackpy/blob/master/README.MD',
      author='LimerBoy',
      author_email='LimerBoyTV@gmail.com',
      license='MIT',
      packages=find_packages(),
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: Microsoft :: Windows",
      ],
      install_requires=[
          'pynput',
      ],
      include_package_data=True,
      zip_safe=False)
