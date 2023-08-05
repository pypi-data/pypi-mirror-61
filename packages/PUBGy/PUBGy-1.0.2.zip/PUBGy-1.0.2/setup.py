from setuptools import setup
with open("README.md") as info:
    desc = info.read()
print(desc)
setup(
   name='PUBGy',
   version='1.0.2',
   description="PUBG API wrapper for Python",
   long_description=desc,
   long_description_content_type="text/markdown",
   author='Discordian',
   author_email='me.discordian@gmail.com',
   packages=['PUBGy'],  #same as name
)
