SPKG is a package programmed in Python for Linux, which can be hosted in repositories to be downloaded and installed through spkgmanager.

To package.spkg, you need create-spkg, a Python script that takes the path of your project (where is the /usr/ path of your build), creates the description of the package, compresses it using tar, and gets it in .spkg format. Then, you need to upload the.spkg to your repository, edit your repo's .list file to indicate the download url and weight of your.spkg package (url, size), and add your .list's download url by entering the "add_repo" command from spkgmanager.

For an example of how to create your SPKG repository, see: https://gitlab.com/Tatakae57/spkg-repo
