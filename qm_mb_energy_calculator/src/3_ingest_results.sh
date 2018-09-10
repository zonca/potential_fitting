TGZ_ARCHIVE=$1
tar xzvf $TGZ_ARCHIVE

BASE_PATH=$(dirname $TGZ_ARCHIVE)

# There could be other job files inside the folder, so better
# get the filename from the archive itself
JOB_FILENAME=$(tar tvf $TGZ_ARCHIVE |  awk '{print $6}')
JOB_PATH=$JOB_FILENAME

echo "Ingesting data from $JOB_PATH into the database"

python database_job_reader.py configurations.db $JOB_PATH $TGZ_ARCHIVE
