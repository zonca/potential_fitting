

job_file = "job_dir/job_1.py"


import subprocess

with open(job_file) as f:
    job_string = f.read()

#run a local test
#subprocess.run(["python", "run_pyscript.py", job_string])

subprocess.run([
    "/root/project/bin/boinc2docker_create_work.py",
    "--rsc_disk_bound",
    "5000000000",
    "--rsc_memory_bound",
    "6000000000",
    "paesanilab/psi4:0.0.4",
    "python",
    "run_pyscript.py",
    job_string
])
