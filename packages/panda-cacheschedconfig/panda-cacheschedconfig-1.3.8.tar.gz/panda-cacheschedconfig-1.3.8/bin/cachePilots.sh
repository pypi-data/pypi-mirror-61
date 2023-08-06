#! /bin/bash
#
# Copy pilot tarballs from cvmfs. Download RC pilot code + pilot 2 dev from Paul's gmsb www area
#
# Authors: Fernando Barreiro Megino, Paul Nilsson

# ----------------------------------------------------------------------
#  FUNCTIONS
# ----------------------------------------------------------------------

gettarball_cvmfs()
{
    # function to get the pilot tarball from cvmfs

    # copy the latest tarballs
    cp /cvmfs/atlas.cern.ch/repo/sw/PandaPilot/tar/pilotcode-PICARD.tar.gz $CACHEPATH/.
    cp /cvmfs/atlas.cern.ch/repo/sw/PandaPilot/tar/pilot2.tar.gz $CACHEPATH/.
}

# ----------------------------------------------------------------------

if [ -f /opt/cacheschedconfig/etc/sysconfig/cachepilot-sysconfig ]; then
    source /opt/cacheschedconfig/etc/sysconfig/cachepilot-sysconfig
fi

# Don't all fire at the same time
if [ "$1" != "--nowait" ]; then
    sleep $(($RANDOM%60))
fi

if [ ! -d $CACHEPATH ]; then
    mkdir -p $CACHEPATH
    if [ $? != "0" ]; then
	echo Failed to create $CACHEPATH
    fi
fi

cd $CACHEPATH

if [ $? == "0" ]; then
    # Copying files from cvmfs
    echo Copying tarball from cvmfs
    gettarball_cvmfs
else
    echo Could not copy the pilot tarball from cvmfs
fi

# ----------------------------------------------------------------------

# Download test builds of the pilot code...
cd $CACHEPATH
for pilot in pilotcode-rc.tar.gz pilot2-dev.tar.gz; do
    curl --connect-timeout 20 --max-time 120 -s -S -O http://project-atlas-gmsb.web.cern.ch/project-atlas-gmsb/${pilot}
done