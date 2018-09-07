job_id = 1
molecule = "H    9.25610245700000e-01   0.00000000000000e+00  -2.48113235200000e-01\nH   -9.30743000000000e-05   0.00000000000000e+00   9.58286909200000e-01\nO   -5.90075300000000e-04   0.00000000000000e+00  -4.52674000000000e-04"
method = "HF"
basis = "STO-3G"
number_of_threads = 6
memory = "500MB"
energy = 0

#try:
#max_threads = int(subprocess.check_output(["grep", "-c", "cores", "/proc/cpuinfo"]))
#print("Maximum threads: {}".format(max_threads))
#except:
#print("Error detecting number of cores. \n Maxium threads: 1")
#max_threads = 1
#
#if number_of_threads > max_threads:
#print("Input number of threads ({}) greater than max threads ({}), limiting number of threads to max threads".format(number_of_threads, max_threads))
#number_of_threads = max_threads
#
#print("Running Job")
#print("Molcule: {}".format(molecule))
#print("Method: {}".format(method))
#print("Basis: {}".format(basis))
#print("Threads {}".format(number_of_threads))
#print("Memory: {}".format(memory))
#
#psi4.core.set_output_file("job_{}.log".format(job_id), False)
#psi4.set_memory(memory)
#psi4.geometry(molecule)
#psi4.set_num_threads(number_of_threads)
#try:
#energy = psi4.energy("{}/{}".format(method, basis))
#print("Energy: {}".format(energy))
success = True
#except ValueError:
#success = False
#print("Iterations failed to Converge")

with open("/root/shared/results/job_{}.out".format(job_id), "w") as out_file:
    out_file.write("Job: {}\n".format(job_id))
    if success:
        out_file.write("Energy: {}".format(energy))
    else:
        out_file.write("Failure")

print("executing")
print("executed")
