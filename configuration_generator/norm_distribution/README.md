Contact: sebrown1@ucsd.edu

Generates configurations for a finite-size system (i.e., molecule, cluster) whose displacements from a given reference geometry/configuration are determined by the normal modes of the system in that geometry.  Generally, the reference geometry is expected to be a (global or local) minimum of the system, though saddles of any order and arbitrary geometries can be handled as well, provided that the normal modes and eigenfrequencies of the system can be evaluated.

By default, the first half of the configurations generated are based on sampling the (quantum) harmonic distribution.  With each configuration generated, the temperature is incremented linearly from 0 kelvin up to the temperature corresponding to the maximum eigenfrequency.  The second half of the configurations generated are based on sampling a variation of the harmonic distribution in which each mode is excited/sampled at a characteristic temperature dependent on its eigenfrequency.  For the j<sup>th</sup> mode, the temperature T<sub>j</sub> at which that mode is sampled is taken to be T<sub>j</sub> = A&hbar;&omega;<sub>j</sub>/k<sub>B</sub>, where the value of A is fixed for all modes.   For each configuration generated, the value of A is incremented linearly from A=0 to A=2.  Note that when A=1, each mode is being sampled at it's Einstein temperature.

Comment 1: I would like to make the code more flexible and give the option of e.g., sampling only the harmonic distribution at a fixed temperature, sampling only the "fixed-A" distribution over a range of A, etc.  This could be particularly useful in generating configurations for clusters, for which the large range of eigenfrequencies results in unreasonable configurations when sampling the harmonic distribution over the range of temperatures described above (see ``EXAMPLES/fluoride-water_trimer/``).

Comment 2: Some of the code is written by other people.  In particular, the code which generates the Sobol sequence is written by John Burkardt (http://people.sc.fsu.edu/~jburkardt/), and the code used to seed the random number generator from the gcc/gnu website (https://gcc.gnu.org/onlinedocs/gfortran/RANDOM_005fSEED.html).

Details can be found in the accompanying pdf forthcoming.pdf.


Required input:
1. Reference geometry/configuration of the molecule or cluster, in xyz file format
2. Eigenfrequencies and normal modes for the reference geometry/configuration, which can be obtained by a typical electronic structure package (e.g., Gaussian09, Molpro, Q-Chem, etc.).  Eigenfrequencies and corresponding modes should be ordered from lowest frequency to highest frequency; imaginary frequencies are denoted with negative signs.  Care must be taken in extracting the normal modes and frequencies, as these packages may differ in how this information is provided, particularly with respect to mass-scaling of the normal mode coordinates.  Included is a bash script to facilitate this for the Q-Chem output files that have been encountered thus far.  This script creates a text file containing the eigenfrequencies in cm<sup>-1</sup>, reduced mass associated with the mode in amu, and the normal mode coordinates in amu<sup>-1/2</sup>.  Each row of normal mode coordinates specifies the x, y, and z components for a particular atom, with the ordering matching the ordering of the atoms in the reference geometry xyz file.  
3. Main input file indicating
  * the name of the file containing the reference geometry
  * the name of the file containing the normal modes and eigenfrequencies
  * full dimensionality of the system (3*`natoms`)
  * dimensionality of the nullspace (6 for nonlinear reference geometries, 5 for linear reference geometries (e.g. carbon dioxide))
  * whether a pseudorandom (`P`) or quasirandom (`Q`) sequence is to be used
  * number of configurations to be generated (a power of 2 is recommended when using the quasirandom sequence)
  * the name of the file which will contain the training set configurations
  * whether a linear or geometric progression is to be used for temperature T and A
  * whether verbose output is desired (prints d(&omega;,T), which reflects the breadth of sampling)

Output:
1. Configurations in xyz file format
2. Output to terminal containing the product U<sup>T</sup>U, where the columns of U are the (mass-scaled) normal modes for the reference geometry (as a test of orthonormality), number of configurations generated, and the CPU time used.  Setting the logical variable 'verbose' equal to '.TRUE.' will also print the temperature and values of d(&omega;,T) for each configuration, where d(&omega;,T) effectively describes the breadth of sampling of each mode as a function of it's frequency &omega; and temperature T.
