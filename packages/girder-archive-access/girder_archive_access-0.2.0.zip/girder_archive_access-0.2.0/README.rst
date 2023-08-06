==============
Archive Access
==============

Access files within zip and tar archives.

Features
--------

This provides access to the contents of files in Girder that are in zip, tar, tar.gz, tgz, or tar.bz2 formats.  It adds a GET file/:id/archive endpoint to list the contents of such an archive and GET file/:id/archive/download to download a component of the archive.

This extends the DICOM viewer plugin so that DICOMs that are stored in an archive are directly viewable in the web client.
