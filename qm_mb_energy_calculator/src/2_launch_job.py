import subprocess

job_file = sys.argv[1]

with open(job_file) as f:
    job_string = f.read()

#run a local test
#subprocess.run(["python", "run_pyscript.py", job_string])

subprocess.run([
    "/root/project/bin/boinc2docker_create_work.py",
    "--rsc_disk_bound",
    "5000000000",
    "--rsc_memory_bound",
    "6000000000", # request 6GB of RAM
    "paesanilab/psi4:0.0.4", # version of the psi4 container, NEVER use latest
    "python",
    "run_pyscript.py",
    job_string
])
