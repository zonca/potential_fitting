
# coding: utf-8

# In[286]:

import sys
import os


# In[287]:

# Check proper if input is provided


# In[288]:

if len(sys.argv) != 3:
    print("Usage: ./script <input.in> <poly-direct.cpp_with_path> \n")
    print("---> Current arguments: " + str(len(sys.argv)) + '\n')
    print("sys.argv[1] = " + sys.argv[0] + '\n')
    print("sys.argv[2] = " + sys.argv[1] + '\n')
    sys.exit()
else:
    name = sys.argv[1]


# In[289]:

# This should be the commandline argument
#name = "A1B2_A1B2.in"
f = open(name, 'r')
mon1 = f.readline().split('\'')[1]
mon2 = f.readline().split('\'')[1]


# In[290]:

# This should be the second command line argument
#directcpp = 'poly-direct.cpp'
directcpp = sys.argv[2]


# In[291]:

# For Andrea:
# Find a way to find the number of atoms in each monomer
# Store them in nat1 and nat2
nat1 = 3
nat2 = 3

# Find the number of sites
nsites1 = 3
nsites2 = 3

# Obtain the lists with the excluded pairs
excl12_a = [[0,1],[0,2]]
excl13_a = [[1,2]]
excl14_a = []

excl12_b = [[0,1],[0,2]]
excl13_b = [[1,2]]
excl14_b = []

#Obtain charges (in the order of input), pols and polfacs
chg_a = ['0.454448','-0.227224','-0.227224']
chg_b = ['0.454448','-0.227224','-0.227224']
pol_a = ['1.43039','0.771519','0.771519']
pol_b = ['1.43039','0.771519','0.771519']
polfac_a = ['1.43039','0.771519','0.771519']
polfac_b = ['1.43039','0.771519','0.771519']

#Ask the user for the max value of k and d
k_min = '0.0'
k_max = '3.0'
k_min_intra = '0.0'
k_max_intra= '2.0'

d_min = '0.0'
d_max = '7.0'
d_min_intra = '0.0'
d_max_intra= '3.0'

# Obtain C6 and d6 from user in the same order as the given pairs AA, AB ...:
C6 = ['310.915','216.702','172.445']
d6 = ['3.20676','3.38985','3.74833']

# Allow user to define Input and output cutoff
# Save them 
r2i = 6.0
r2o = 7.0

# FInd a way to get the degree
degree = 3
# Find a way to get the number ov variables
nvars = 15
# Find a way to get the size of the polynomial
npoly = 134

# Define kind of variables for intra, inter and lone pairs
var_intra = 'exp'
var_lp = 'coul'
var_inter = 'exp'

# Define Energy Range for the fitting
E_range = '30.0'


# In[292]:

types_a = list(mon1)
types_b = list(mon2)
print(types_a)
print(types_b)


# In[293]:

# Generating the non linear parameter list
nlparam = []
t1 = []
# Monomer 1 parameters
for i in range(0,len(types_a),2):
    for j in range(int(types_a[i+1])):
        t1.append(types_a[i])
t2 = []
# Monomer 2 parameters
for i in range(0,len(types_b),2):
    for j in range(int(types_b[i+1])):
        t2.append(types_b[i])
print(t1)
print(t2)


# In[294]:

# Appending for mon1
for i in range(len(t1)):
    for j in range(1,len(t1)):
        for nlp in ['d','k']:
            const_intra = nlp + '_intra_' + t1[i] + t1[j]
            if not const_intra in nlparam:
                nlparam.append(const_intra)

# Appending for mon2
for i in range(len(t2)):
    for j in range(1,len(t2)):
        for nlp in ['d','k']:
            const_intra = nlp + '_intra_' + t2[i] + t2[j]
            if not const_intra in nlparam:
                nlparam.append(const_intra)

# Intermolecular
for i in range(len(t1)):
    for j in range(len(t2)):
        p = sorted([t1[i],t2[j]])
        for nlp in ['d','k']:
            const_inter = nlp + '_' + p[0] + p[1]
            if not const_inter in nlparam:
                nlparam.append(const_inter)

# Getting the pairs
pairs = []
for i in range(len(t1)):
    for j in range(len(t2)):
        p = sorted([t1[i],t2[j]])
        ps = p[0] + p[1]
        if not ps in pairs:
            pairs.append(ps)

print(nlparam)
print(pairs)    


# In[295]:

# Save number in num_nonlinear
num_nonlinear = len(nlparam)



# ## Creating mon1.h and mon2.h

# In[296]:

mon1_class = open('mon1.h','w')

a="""
#ifndef MON1_H
#define MON1_H
#include "molecule.h"

namespace x   {

   class mon1 : public molecule {
      public :
      mon1();
      ~mon1();
      
      mon1(double* crd);
      double* set_sitecrds(double* xyz);            
      double* set_charges(double* xyz);
      double* set_polfacs(double* atmpolar);
      double* set_pol();
      void allocate();

      int get_nsites();
      double* get_sitecrds();
      double* get_charges();
      double* get_polfacs();
      double* get_pol();

      excluded_set_type::iterator get_begin_12();
      excluded_set_type::iterator get_begin_13();
      excluded_set_type::iterator get_begin_14();
      excluded_set_type::iterator get_end_12();
      excluded_set_type::iterator get_end_13();
      excluded_set_type::iterator get_end_14();

   };   
}
#endif
"""

mon1_class.write(str(a))
mon1_class.close()


# In[297]:

mon1_class = open('mon2.h','w')

a="""
#ifndef MON2_H
#define MON2_H
#include "molecule.h"

namespace x   {

   class mon2 : public molecule {
      public :
      mon2();
      ~mon2();
      
      mon2(double* crd);
      double* set_sitecrds(double* xyz);            
      double* set_charges(double* xyz);
      double* set_polfacs(double* atmpolar);
      double* set_pol();
      void allocate();

      int get_nsites();
      double* get_sitecrds();
      double* get_charges();
      double* get_polfacs();
      double* get_pol();

      excluded_set_type::iterator get_begin_12();
      excluded_set_type::iterator get_begin_13();
      excluded_set_type::iterator get_begin_14();
      excluded_set_type::iterator get_end_12();
      excluded_set_type::iterator get_end_13();
      excluded_set_type::iterator get_end_14();

   };   
}
#endif
"""

mon1_class.write(a)
mon1_class.close()


# ## Creating their cpp files

# In[298]:

ff = open('mon1.cpp','w')

a = """
#include "mon1.h"
#include "ps.h"
#include <algorithm>
#include <cstddef>
#include "fit-constants.h"

//#define VERBOSE
#ifdef VERBOSE 
#include <iostream>
#endif

const double CHARGECON = constants::CHARGECON;

// NOTE: ASSUMING ABB

namespace x  {

  mon1::mon1() { }

  mon1::~mon1() {
    delete[] memory;
  }

  mon1::mon1( double* crd) {
    
    nsites = """ + str(nsites1) + """;  
    
    allocate();
    
    sitecrds = set_sitecrds(crd);
    atmpolar = set_pol();
    charge = set_charges(crd);
    polfac = set_polfacs(atmpolar);

    // Excluded pairs
"""
ff.write(a)
for p in excl12_a:
    ff.write('    excluded12.insert(std::make_pair(' + str(p[0]) + ',' + str(p[1]) + '));\n')
for p in excl13_a:
    ff.write('    excluded13.insert(std::make_pair(' + str(p[0]) + ',' + str(p[1]) + '));\n')
for p in excl14_a:
    ff.write('    excluded14.insert(std::make_pair(' + str(p[0]) + ',' + str(p[1]) + '));\n')
a = """

  }

  double* mon1::set_charges(double* atmcrds) {
    charge = memory;
"""
ff.write(a)
for i in range(len(chg_a)):
    ff.write('    charge[' + str(i) + '] = ' + chg_a[i] + '*CHARGECON;\n')
a = """

    return charge;
  }
  
  double* mon1::set_pol() {
    atmpolar = memory + nsites + nsites*3;
"""
ff.write(a)
for i in range(len(pol_a)):
    ff.write('    atmpolar[' + str(i) + '] = ' + pol_a[i] + ';\n')
a = """
    return atmpolar;
  }

  double* mon1::set_polfacs(double* atmpol) {
    polfac = memory + nsites + nsites*3 + nsites;
    
"""
ff.write(a)
for i in range(len(polfac_a)):
    ff.write('    polfac[' + str(i) + '] = ' + polfac_a[int(i)] + ';\n')
a = """
    return polfac;
  }

  double* mon1::set_sitecrds(double* atmcrds) {
    sitecrds = memory + nsites;
    
// ##DEFINE HERE## ficticious site coordinates
    return atmcrds;  
  }

  void mon1::allocate() {
    memory = new double [nsites  //charge
      + nsites*3  //site coordinates
      + nsites  //polarizabilities 
      + nsites];  //polfac
    }

    int mon1::get_nsites() { return nsites; }
    double* mon1::get_charges() { return charge; }
    double* mon1::get_sitecrds() { return sitecrds; }
    double* mon1::get_pol() { return atmpolar; }
    double* mon1::get_polfacs() { return polfac; }

    excluded_set_type::iterator mon1::get_begin_12() { return excluded12.begin(); }
    excluded_set_type::iterator mon1::get_begin_13() { return excluded13.begin(); }
    excluded_set_type::iterator mon1::get_begin_14() { return excluded14.begin(); }
    excluded_set_type::iterator mon1::get_end_12() { return excluded12.end(); }
    excluded_set_type::iterator mon1::get_end_13() { return excluded13.end(); }
    excluded_set_type::iterator mon1::get_end_14() { return excluded14.end(); }

} // namespace x
"""

ff.write(a)
ff.close()


# In[299]:

ff = open('mon2.cpp','w')

a = """
#include "mon2.h"
#include "ps.h"
#include <algorithm>
#include <cstddef>
#include "fit-constants.h"

//#define VERBOSE
#ifdef VERBOSE 
#include <iostream>
#endif

const double CHARGECON = constants::CHARGECON;

// NOTE: ASSUMING ABB

namespace x  {

  mon2::mon2() { }

  mon2::~mon2() {
    delete[] memory;
  }

  mon2::mon2( double* crd) {
    
    nsites = """ + str(nsites2) + """;  
    
    allocate();
    
    sitecrds = set_sitecrds(crd);
    atmpolar = set_pol();
    charge = set_charges(crd);
    polfac = set_polfacs(atmpolar);

    // Excluded pairs
"""
ff.write(a)
for p in excl12_b:
    ff.write('    excluded12.insert(std::make_pair(' + str(p[0]) + ',' + str(p[1]) + '));\n')
for p in excl13_b:
    ff.write('    excluded13.insert(std::make_pair(' + str(p[0]) + ',' + str(p[1]) + '));\n')
for p in excl14_b:
    ff.write('    excluded14.insert(std::make_pair(' + str(p[0]) + ',' + str(p[1]) + '));\n')
a = """

  }

  double* mon2::set_charges(double* atmcrds) {
    charge = memory;
"""
ff.write(a)
for i in range(len(chg_b)):
    ff.write('    charge[' + str(i) + '] = ' + chg_b[i] + '*CHARGECON;\n')
a = """

    return charge;
  }
  
  double* mon2::set_pol() {
    atmpolar = memory + nsites + nsites*3;
"""
ff.write(a)
for i in range(len(pol_b)):
    ff.write('    atmpolar[' + str(i) + '] = ' + pol_b[i] + ';\n')
a = """
    return atmpolar;
  }

  double* mon2::set_polfacs(double* atmpol) {
    polfac = memory + nsites + nsites*3 + nsites;
    
"""
ff.write(a)
for i in range(len(polfac_b)):
    ff.write('    polfac[' + str(i) + '] = ' + polfac_b[i] + ';\n')
a = """
    return polfac;
  }

  double* mon2::set_sitecrds(double* atmcrds) {
    sitecrds = memory + nsites;
    
// ##DEFINE HERE## ficticious site coordinates
    return atmcrds;  
  }

  void mon2::allocate() {
    memory = new double [nsites  //charge
      + nsites*3  //site coordinates
      + nsites  //polarizabilities 
      + nsites];  //polfac
    }

    int mon2::get_nsites() { return nsites; }
    double* mon2::get_charges() { return charge; }
    double* mon2::get_sitecrds() { return sitecrds; }
    double* mon2::get_pol() { return atmpolar; }
    double* mon2::get_polfacs() { return polfac; }

    excluded_set_type::iterator mon2::get_begin_12() { return excluded12.begin(); }
    excluded_set_type::iterator mon2::get_begin_13() { return excluded13.begin(); }
    excluded_set_type::iterator mon2::get_begin_14() { return excluded14.begin(); }
    excluded_set_type::iterator mon2::get_end_12() { return excluded12.end(); }
    excluded_set_type::iterator mon2::get_end_13() { return excluded13.end(); }
    excluded_set_type::iterator mon2::get_end_14() { return excluded14.end(); }

} // namespace x
"""

ff.write(a)
ff.close()


# ## Create training_set.h/cpp files

# In[300]:

ff = open('training_set.h','w')
a = """
#ifndef TRAINING_SET_H
#define TRAINING_SET_H

#include <cstdlib>
#include <vector>

namespace tset {

struct dimer {
    double energy_total;
    double energy_twobody;
    double energy_onebody[2];
    
    // Note: XYZ is for the real sites
"""
ff.write(a)
ff.writelines("    double xyz[" + str((nat1 + nat2)*3) + "];\n")
a = """
    double mb_total_energy() const
    {
        return energy_twobody + energy_onebody[0] + energy_onebody[1];
    }
};

size_t load_dimers(const char* filename, std::vector<dimer>& ts);

} // namespace tset

#endif // TRAINING_SET_H
"""
ff.write(a)
ff.close()


# ## X2B h file

# In[301]:

hname = "x2b_" + mon1 + "_" + mon2 + "_v1x.h"
polyhname = "poly_2b_" + mon1 + "_" + mon2 + "_v1x.h"
polyhname2 = "poly_2b_" + mon1 + "_" + mon2 + ".h"
defname = "X2B_" + mon1 + "_" + mon2 + "_V1X_H"
ff = open(hname,'w')
ff.write('#ifndef ' + defname + '\n')
ff.write('#define ' + defname + '\n \n')
ff.write('#include "' + polyhname + '" \n')
ff.write('#include "' + polyhname2 + '" \n \n')

a = """
#include <iostream>
////////////////////////////////////////////////////////////////////////////////

namespace x2b_""" + mon1 + "_" + mon2 + """ {

//----------------------------------------------------------------------------//

"""
ff.write(a)
ff.write('struct x2b_' + mon1 + "_" + mon2 + "_v1x { \n")
a = """
    typedef mb_system::poly_model poly_type;
    typedef mb_system_fit::poly_model poly_type_fit;


    static std::string name();
    void load_netcdf(const char*);

    // returns 2B contribution only
    // XYZ is for the real sites
"""
ff.write(a)
ff.write('//    double operator()(const double xyz[' + str(3*(nat1 + nat2)) + '], double grd[' + str(3*(nat1 + nat2)) + ']) const; \n')
ff.write('    double operator()(const double xyz[' + str(3*(nat1 + nat2)) + ']) const; \n')
a = """
    double eval(const double* mon1, const double* mon2) const;
    double eval(const double* mon1, const double* mon2, double* g1, double* g2) const;
    void cart_to_vars(const double xyz[""" + str(3*(nat1 + nat2)) + """], double* vars, double& s, double& gs) const;
    
    // For fitting purposes
    size_t get_nvars() {return poly_type::n_vars;}
    size_t get_num_nonlinear_params() {return """ + str(num_nonlinear) + """;}
    void set_nonlinear_parameters(const double*);
    void set(const double* xxx);
    void get_nonlinear_parameters(double*);
    bool nonlinear_parameters_out_of_range() const;
    inline double basis(const double xyz[""" + str(3*(nat1 + nat2)) + """], double*) const; //basis polynomials
    inline size_t nparams() {
      return poly_type::size;
    }
    

    inline void as_cdl(std::ostream&) const;
    void write_cdl(std::ostream&, unsigned, unsigned, const double*) const;
    
private:

"""
ff.write(a)
for nl in nlparam:
    ff.write("    double m_" + nl + ";\n")
a = """
protected:
    double m_r2i = """ + str(r2i) + """;
    double m_r2f = """ + str(r2o) + """;

    double f_switch(const double&, double&) const; // At1_a -- At1_b separation

private:
    double m_poly[poly_type::size];
};

// For fitting
inline void x2b_""" + mon1 + "_" + mon2 + """_v1x::as_cdl(std::ostream& os) const
{
    write_cdl(os, """ + str(degree) + """, poly_type::size, m_poly);
}


inline double
x2b_""" + mon1 + "_" + mon2 + """_v1x::basis(const double xyz[""" + str(3*(nat1 + nat2)) + """], double* mmm) const //mmm = monomials?
{
    double v[poly_type::n_vars], s, gs;

    cart_to_vars(xyz, v, s, gs);

    poly_type_fit polyn;
    polyn.eval(v, mmm);
    for (unsigned n = 0; n < poly_type::size; ++n)
        mmm[n] *= s;

    return 0; // we will substract electrostatics and dispersion in the main
}

//----------------------------------------------------------------------------//

} // namespace x2b_""" + mon1 + "_" + mon2 + """

////////////////////////////////////////////////////////////////////////////////

#endif 
"""
ff.write(a)
ff.close()


# ## CPP file

# In[302]:

cppname = "x2b_" + mon1 + "_" + mon2 + "_v1x.cpp"
ff = open(cppname,'w')
a = """
#include <cmath>
#include <cassert>
#include <cstdlib>
#include <iomanip>

#include <netcdf.h>

#include "stuff.h"
#include "constants.h"
"""
ff.write(a)
ff.write('#include "' + hname + '" \n \n')
a = """
////////////////////////////////////////////////////////////////////////////////

namespace {

//----------------------------------------------------------------------------//

void error(int kode) {

    std::cerr << " ** Fatal Error in x2b_""" + mon1 + "_" + mon2 + """_v1x::load_netcdf() ** :" 
              << nc_strerror(kode) << std::endl;
    std::exit(EXIT_FAILURE);
}

//----------------------------------------------------------------------------//

struct variable {
    double v_exp(const double& r0, const double& k,
                 const double * p1, const double * p2 );

    double v_coul(const double& r0, const double& k,
                  const double * p1, const double * p2 );

    double g[3]; // diff(value, p1 - p2)
};

//- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - //

double variable::v_exp(const double& r0, const double& k,
                       const double * p1, const double * p2)
{
    g[0] = p2[0] - p1[0];
    g[1] = p2[1] - p1[1];
    g[2] = p2[2] - p1[2];

    const double r = std::sqrt(g[0]*g[0] + g[1]*g[1] + g[2]*g[2]);

    const double exp1 = std::exp(k*(r0 - r));
    const double gg = - k*exp1/r;

    g[0] *= gg;
    g[1] *= gg;
    g[2] *= gg;

    return exp1;
}

//- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - //

double variable::v_coul(const double& r0, const double& k,
                        const double * p1, const double * p2)
{
    g[0] = p2[0] - p1[0];
    g[1] = p2[1] - p1[1];
    g[2] = p2[2] - p1[2];

    const double rsq = g[0]*g[0] + g[1]*g[1] + g[2]*g[2];
    const double r = std::sqrt(rsq);

    const double exp1 = std::exp(k*(r0 - r));
    const double rinv = 1.0/r;
    const double val = exp1*rinv;

    const double gg = - (k + rinv)*val*rinv;

    g[0] *= gg;
    g[1] *= gg;
    g[2] *= gg;

    return val;
}

} // namespace

////////////////////////////////////////////////////////////////////////////////

namespace x2b_""" + mon1 + "_" + mon2 + """ {

//----------------------------------------------------------------------------//


std::string x2b_""" + mon1 + "_" + mon2 + """_v1x::name() {
    return "x2b_""" + mon1 + "_" + mon2 + """_v1x";
}
"""
ff.write(a)
ff.write('void x2b_' + mon1 + '_' + mon2 + '_v1x::set_nonlinear_parameters(const double* xxx) \n { \n ')
for nl in nlparam:
    ff.write("    m_" + nl + " = *xxx++; \n")
a = """
}

//----------------------------------------------------------------------------//

"""
ff.write(a)
ff.write('void x2b_' + mon1 + '_' + mon2 + '_v1x::get_nonlinear_parameters(double* xxx) \n { \n ')
for nl in nlparam:
    ff.write("   *xxx++ = m_" + nl + "; \n")
a = """
}

//----------------------------------------------------------------------------//

void x2b_""" + mon1 + "_" + mon2 + """_v1x::set(const double* xxx) {
  std::copy(xxx, xxx + nparams(), m_poly);
}

//----------------------------------------------------------------------------//


void x2b_""" + mon1 + "_" + mon2 + """_v1x::write_cdl(std::ostream& os, unsigned DEG,
                              unsigned npoly, const double* poly) const
{
    using namespace std;

    ios::fmtflags saved_flags = os.flags();

    os << setprecision(15) << scientific
       << "netcdf x2b_""" + mon1 + "_" + mon2 + """_v1x {" << endl
       << "  // global attributes " << endl
       << "  :name = \\"x2b_""" + mon1 + "_" + mon2 + """_v1x<" << DEG << ">\\";" << endl;

    // x2b_""" + mon1 + "_" + mon2 + """_v1x::as_cdl(os);
"""
ff.write(a)
ff.write('    os ')
for nl in nlparam:
    ff.write('       << "  :' + nl + ' = " << setw(22) << m_' + nl +  ' << "; // A^(-1))" << endl \n')
a = """
         << "  :r2i = " << setw(22) << m_r2i << "; // A" << endl
         << "  :r2f = " << setw(22) << m_r2f << "; // A" << endl
         << "  dimensions:" << endl
         << "  poly = " << npoly << ";" << endl
         << "  variables:" << endl
         << "    double poly(poly);" << endl
         << "data:" << endl;

    os << "poly =" << endl;

    {
        unsigned n(0);
        for (n = 0; n + 1 < npoly; ++n)
            os << std::setw(22) << poly[n] << ", // " << n << endl;
        os <<  std::setw(22) << poly[n] << "; // " << n << endl << endl;
    }

    os << "}" << endl;
    os.flags(saved_flags);
}

//----------------------------------------------------------------------------//
"""
ff.write(a)
ff.write('bool x2b_' + mon1 + '_' + mon2 + '_v1x::nonlinear_parameters_out_of_range() const { \n')
ff.write('    const double k_min =  ' + k_min + ' ;\n')
ff.write('    const double k_max =  ' + k_max + ' ;\n')
ff.write('    const double k_min_intra =  ' + k_min_intra + ' ;\n')
ff.write('    const double k_max_intra =  ' + k_max_intra + ' ;\n\n')

ff.write('    const double d_min =  ' + d_min + ' ;\n')
ff.write('    const double d_max =  ' + d_max + ' ;\n')
ff.write('    const double d_min_intra =  ' + d_min_intra + ' ;\n')
ff.write('    const double d_max_intra =  ' + d_max_intra + ' ;\n\n')

ff.write('return false')
for nl in nlparam:
    if nl.startswith('d'):
        if (nl.startswith('d_intra')):
            ff.write('\n       || m_' + nl + ' < d_min_intra ')
            ff.write('\n       || m_' + nl + ' > d_max_intra ')
        else:
            ff.write('\n       || m_' + nl + ' < d_min ')
            ff.write('\n       || m_' + nl + ' > d_max ')
    else:
        if (nl.startswith('k_intra')):
            ff.write('\n       || m_' + nl + ' < k_min_intra ')
            ff.write('\n       || m_' + nl + ' > k_max_intra ')
        else:
            ff.write('\n       || m_' + nl + ' < k_min ')
            ff.write('\n       || m_' + nl + ' > k_max ')
    
ff.write('; \n')            
a = """

}

// ##DEFINE HERE## need to think how to generalize this function...

"""
ff.write(a)
ff.write('void  x2b_' + mon1 + '_' + mon2 + '_v1x::cart_to_vars(const double* xyz, double* v, double& s, double& gs) const { \n')
ff.write('    // NOTE: XYZ contains ONLY the real sites. The lone pairs etc are calculated here \n')

nc = 0
set_m1 = []
set_m2 = []
for i in range(0,len(types_a),2):
    n = 1
    for j in range(int(types_a[i+1])):
        ff.write('    const double* ' + types_a[i] + '_' + str(n) + '_a' + '= xyz + ' + str(3 * nc) + ';\n')
        set_m1.append(types_a[i] + '_' + str(n) + '_a')
        n = n + 1
        nc = nc + 1
ff.write('\n')
for i in range(0,len(types_b),2):
    n = 1
    for j in range(int(types_b[i+1])):
        ff.write('    const double* ' + types_b[i] + '_' + str(n) + '_b' + '= xyz + ' + str(3 * nc) + ';\n')
        set_m2.append(types_b[i] + '_' + str(n) + '_b')
        n = n + 1
        nc = nc + 1

a = """
// ##DEFINE HERE## the lone pairs if any
    // double Xa1[3], Xa2[3];

    // xpoints(m_in_plane_gamma, m_out_of_plane_gamma, O, Xa1, Xa2);
    
    variable vr[15];
    using x2o::distance;
    
"""
ff.write(a)
nv = 0
# Intramolecular distances:
for i in range(0,len(set_m1) - 1):
    for j in range(i + 1,len(set_m1)):
        ti = set_m1[i].split('_')[0]
        tj = set_m1[j].split('_')[0]
        t = ''.join(sorted(ti + tj))
        ff.write('    v[' + str(nv) + ']  = vr[' + str(nv) + '].v_' + var_intra + '(m_d_intra_' + t + ', m_k_intra_' + t + ', ' + set_m1[i] + ', ' + set_m1[j] + ');\n')
        nv = nv + 1
ff.write('\n')
for i in range(0,len(set_m2) - 1):
    for j in range(i + 1,len(set_m2)):
        ti = set_m2[i].split('_')[0]
        tj = set_m2[j].split('_')[0]
        t = ''.join(sorted(ti + tj))
        ff.write('    v[' + str(nv) + ']  = vr[' + str(nv) + '].v_' + var_intra + '(m_d_intra_' + t + ', m_k_intra_' + t + ', ' + set_m2[i] + ', ' + set_m2[j] + ');\n')
        nv = nv + 1
ff.write('\n')
# Intermolecular distances
for i in range(0,len(set_m1)):
    for j in range(0,len(set_m2)):
        ti = set_m1[i].split('_')[0]
        tj = set_m2[j].split('_')[0]
        t = ''.join(sorted(ti + tj))
        ff.write('    v[' + str(nv) + ']  = vr[' + str(nv) + '].v_' + var_inter + '(m_d_' + t + ', m_k_' + t + ', ' + set_m1[i] + ', ' + set_m2[j] + ');\n')
        nv = nv + 1
    ff.write('\n')

a = """
    s = f_switch(distance(""" + set_m1[0] + ', ' + set_m2[0] + """), gs);
    
#define PR(x)
  PR(s);
"""
ff.write(a)
for i in range(nv):
    ff.write('  PR(v[' + str(i) + ']);\n')
a = """
} 

//----------------------------------------------------------------------------//

//----------------------------------------------------------------------------//

void x2b_""" + mon1 + "_" + mon2 + """_v1x::load_netcdf(const char* fn)
{
    assert(fn);

    int rc, ncid;
    if ((rc = nc_open(fn, NC_NOWRITE, &ncid)))
        error(rc);

#   define RETRIEVE(name) \\
    if ((rc = nc_get_att_double(ncid, NC_GLOBAL, #name , &m_##name))) \\
        error(rc);
"""
ff.write(a)
for nl in nlparam:
    ff.write("    RETRIEVE(" + nl + ")\n")
a = """

    RETRIEVE(r2i)
    RETRIEVE(r2f)

#   undef RETRIEVE

    int varid;

    if ((rc = nc_inq_varid(ncid, "poly", &varid)))
        error(rc);

    for (size_t n = 0; n < poly_type::size; ++n) {
        if ((rc = nc_get_var1_double(ncid, varid, &n, m_poly + n)))
            error(rc);
    }

    if ((rc = nc_close(ncid)))
        error(rc);
}

//----------------------------------------------------------------------------//

double x2b_""" + mon1 + "_" + mon2 + """_v1x::f_switch(const double& r, double& g) const
{
    if (r > m_r2f) {
        g = 0.0;
        return 0.0;
    } else if (r > m_r2i) {
        const double t1 = M_PI/(m_r2f - m_r2i);
        const double x = (r - m_r2i)*t1;
        g = - std::sin(x)*t1/2.0;
        return (1.0 + std::cos(x))/2.0;
    } else {
        g = 0.0;
        return 1.0;
    }
}

//----------------------------------------------------------------------------//

double x2b_""" + mon1 + "_" + mon2 + """_v1x::eval(const double* mon1, const double* mon2 ) const
{
    // the switch

    // ##DEFINE HERE## right now it assumes 1st atom of each monomer
    const double d12[3] = {mon1[0] -  mon2[0],
                           mon1[1] -  mon2[1],
                           mon1[2] -  mon2[2]};

    const double r12sq = d12[0]*d12[0] + d12[1]*d12[1] + d12[2]*d12[2];
    const double r12 = std::sqrt(r12sq);

    if (r12 > m_r2f)
        return 0.0;

    double xcrd[""" + str(3*(nat1 + nat2)) + """]; // coordinates of real sites ONLY

    std::copy(mon1, mon1 + """ + str(3*(nat1)) + """, xcrd);
    std::copy(mon2, mon2 + """ + str(3*(nat2)) + """, xcrd + """ + str(3*(nat1)) + """);
    
    double v[15]; 
    double sw = 0.0;
    double gsw = 0.0;
    cart_to_vars(xcrd, v, sw, gsw); 
    
    const double E_poly = mb_system::poly_model::eval(m_poly, v);

    return sw*E_poly;
}

double x2b_""" + mon1 + "_" + mon2 + """_v1x::operator()(const double crd[18]) const
{
    const double E_poly = eval(crd, crd + """ + str(3*(nat1)) + """);

    return E_poly;
}

} // namespace x2b_""" + mon1 + "_" + mon2 + """

////////////////////////////////////////////////////////////////////////////////
"""
ff.write(a)
ff.close()


# ## Dispersion.h

# In[303]:

hname = "dispersion.h"
ff = open(hname,'w')
a = """
#ifndef DISPERSION_H
#define DISPERSION_H

#include "tang-toennies.h"
#include <cmath>
#include <algorithm>



struct x2b_disp {
  x2b_disp();
  x2b_disp(double *, double * , size_t, size_t);
  ~x2b_disp();

"""
ff.write(a)
for i in range(len(pairs)):
    ff.write('  const double m_C6_' + pairs[i] + ' = ' + C6[i] + ' ; \n')
for i in range(len(pairs)):
    ff.write('  const double m_d6_' + pairs[i] + ' = ' + d6[i] + ' ; \n')
    
a = """

  const double m_C8 = 0.0;
  const double m_d8 = 0.0;

  const double if6 = 1.0/x2o::factorial<6>();
  const double if8 = 1.0/x2o::factorial<8>();

  double * xyz1;
  double * xyz2;

  double get_dispersion();


  inline double x6(const double& C6, const double& d6,
                  const double& C8, const double& d8,
                  const double* p1, const double* p2,
                        double* g1,       double* g2)
  {
    const double dx = p1[0] - p2[0];
    const double dy = p1[1] - p2[1];
    const double dz = p1[2] - p2[2];

    const double rsq = dx*dx + dy*dy + dz*dz;
    const double r = std::sqrt(rsq);

    const double d6r = d6*r;
    const double tt6 = x2o::tang_toennies(6, d6r);

    const double d8r = d8*r;
    const double tt8 = x2o::tang_toennies(8, d8r);


    const double inv_rsq = 1.0/rsq;
    const double inv_r6 = inv_rsq*inv_rsq*inv_rsq;
    const double inv_r8 = inv_r6*inv_rsq;

    const double e6 = C6*tt6*inv_r6;
    const double e8 = C8*tt8*inv_r8;

    const double grd = (6*e6 + 8*e8)*inv_rsq
        - (C6*std::pow(d6, 7)*if6*std::exp(-d6r)
        +  C8*std::pow(d8, 9)*if8*std::exp(-d8r))/r;

    g1[0] += dx*grd;
    g2[0] -= dx*grd;

    g1[1] += dy*grd;
    g2[1] -= dy*grd;

    g1[2] += dz*grd;
    g2[2] -= dz*grd;

    return - (e6 + e8);
  }

  inline double x6(const double& C6, const double& d6,
                  const double& C8, const double& d8,
                  const double* p1, const double* p2)
  {
    const double dx = p1[0] - p2[0];
    const double dy = p1[1] - p2[1];
    const double dz = p1[2] - p2[2];

    const double rsq = dx*dx + dy*dy + dz*dz;
    const double r = std::sqrt(rsq);

    const double d6r = d6*r;
    const double tt6 = x2o::tang_toennies(6, d6r);

    const double d8r = d8*r;
    const double tt8 = x2o::tang_toennies(8, d8r);


    const double inv_rsq = 1.0/rsq;
    const double inv_r6 = inv_rsq*inv_rsq*inv_rsq;
    const double inv_r8 = inv_r6*inv_rsq;

    const double e6 = C6*tt6*inv_r6;
    const double e8 = C8*tt8*inv_r8;

    return - (e6 + e8);
  }
};

#endif

"""
ff.write(a)
ff.close()


# ## dispersion.cpp

# In[304]:

cppname = "dispersion.cpp"
ff = open(cppname,'w')
a = """
#include "dispersion.h"

x2b_disp::x2b_disp() {}
x2b_disp::~x2b_disp() {
  delete[] xyz1;
  delete[] xyz2;
}

x2b_disp::x2b_disp(double * c1, double * c2, size_t n1, size_t n2) {
  xyz1 = new double[3*n1];
  xyz2 = new double[3*n2];
  std::copy(c1, c1 + 3*n1, xyz1);
  std::copy(c2, c2 + 3*n2, xyz2);
}

double x2b_disp::get_dispersion() {

  double disp = 0.0;
"""
ff.write(a)

nc = 0
set_m1 = []
set_m2 = []
for i in range(0,len(types_a),2):
    n = 1
    for j in range(int(types_a[i+1])):
        ff.write('  const double* ' + types_a[i] + '_' + str(n) + '_a' + '= xyz1 + ' + str(3 * nc) + ';\n')
        set_m1.append(types_a[i] + '_' + str(n) + '_a')
        n = n + 1
        nc = nc + 1
ff.write('\n')

nc = 0
for i in range(0,len(types_b),2):
    n = 1
    for j in range(int(types_b[i+1])):
        ff.write('  const double* ' + types_b[i] + '_' + str(n) + '_b' + '= xyz2 + ' + str(3 * nc) + ';\n')
        set_m2.append(types_b[i] + '_' + str(n) + '_b')
        n = n + 1
        nc = nc + 1
ff.write('\n')

for i in range(0,len(set_m1)):
    for j in range(0,len(set_m2)):
        ti = set_m1[i].split('_')[0]
        tj = set_m2[j].split('_')[0]
        t = ''.join(sorted(ti + tj))
        ff.write('  disp += x6(m_C6_' + t + ', m_d6_' + t + ', m_C8, m_d8, ' + set_m1[i] + ', ' + set_m2[j] + ');\n')
        
    ff.write('\n')
a = """
  return disp;
}
"""
ff.write(a)
ff.close()


# ## Fitting routine

# In[311]:

cppname = "fit-2b.cpp"
ff = open(cppname,'w')
a = """
#include <cmath>
#include <cassert>
#include <cstdlib>

#include <fstream>
#include <sstream>
#include <iomanip>
#include <iostream>
#include <stdexcept>

#include <gsl/gsl_multimin.h>

#define RIDGE_REGRESSION 1

#ifdef RIDGE_REGRESSION
#   include "rwlsq.h"
#else
#   include "wlsq.h"
#endif

#include "mon1.h"
#include "mon2.h"
#include "fit-utils.h"
#include "training_set.h"
#include "x2b_""" + mon1 + """_""" + mon2 + """_v1x.h"
#include "electrostatics.h"
#include "coulomb.h"
#include "dispersion.h"


#define dont_be_VERBOSE yes

//#define DEBUG 

#ifdef DEBUG
#define PR(x) std::cout << #x << ": " << (x) << std::endl;
#else
#define PR(x)
#endif /* DEBUG */

using namespace std;

namespace {

static x2b_""" + mon1 + """_""" + mon2 + """::x2b_""" + mon1 + """_""" + mon2 + """_v1x model;


#ifdef RIDGE_REGRESSION
const double alpha = 0.0005;
#endif

// ##DEFINE HERE## energy range
const double E_range = """ + E_range + """; // kcal/mol

//----------------------------------------------------------------------------//

static std::vector<tset::dimer> training_set;
static std::vector<double> elec_e;
static std::vector<double> disp_e;
static double* ts_weights = 0;

namespace linear {

//----------------------------------------------------------------------------//

static double* A(0);
static double* y(0);
static double* params(0);

//----------------------------------------------------------------------------//

void allocate()
{
    A = new double[training_set.size()*model.nparams()];
    y = new double[training_set.size()];

    params = new double[model.nparams()];
}

//----------------------------------------------------------------------------//

double compute_chisq(const gsl_vector* X, void* unused)
{
    model.set_nonlinear_parameters(X->data);

    if (model.nonlinear_parameters_out_of_range())
        return 1.0e+6;

    PR(model_type::nparams())
    for (size_t n = 0; n < training_set.size(); ++n) {
        double mmm[model.nparams()];
        y[n] = training_set[n].energy_twobody
               - model.basis(training_set[n].xyz, mmm);
        for (size_t p = 0; p < model.nparams(); ++p) {
            A[p + n*model.nparams()] = mmm[p];
        }
    }

#   ifdef VERBOSE
    std::cout << "=== calling wlsq::solve() ["
              << kit::wlsq::implementation()
              << "] ===" << std::endl;
#   endif

    double chisq;

//    try {
#     ifdef RIDGE_REGRESSION
      double penaltysq;
      kit::rwlsq::solve(training_set.size(), model.nparams(),
                        A, y, ts_weights, alpha, params, chisq, penaltysq);

      std::cout << "<#> chisq = " << chisq
                << " : penaltysq = " << penaltysq
                << std::endl;
#     else
      int rank;
      kit::wlsq::solve(training_set.size(), model_type::nparams(),
                       A, y, ts_weights, params, chisq, rank);
      std::cout << "<#> chisq = " << chisq
                << " : rank = " << rank
                << std::endl;
#     endif

      if (!gsl_finite (chisq)) {
        return 10000000.0;
      }
//    } catch (const std::exception& e) {
//      return 1000000.0;
//    }
#   ifdef VERBOSE
    std::cout << "\\n--> chisq = " << chisq
              << "\\n-->  rank = " << rank
              << '\\n' << std::endl;
#   endif

    return chisq;
}

//----------------------------------------------------------------------------//

} // namespace linear

////////////////////////////////////////////////////////////////////////////////

} // namespace

////////////////////////////////////////////////////////////////////////////////

int main(int argc, char** argv) {
    if (argc < 2) {
        std::cerr << "usage: fit-2b ts1 ..."
                  << std::endl;
        return 0;
    }

      double x0[""" + str(len(nlparam)) + """];
"""
ff.write(a)
for i in range(len(nlparam)):
    if nlparam[i].startswith('d'):
        if nlparam[i].startswith('d_intra'):
            ff.write('      x0[' + str(i) + '] = ((double) rand() / (RAND_MAX)) * ' + str(float(d_max_intra) - float(d_min_intra)) + ' + ' + d_min_intra + ';\n')
        else:
            ff.write('      x0[' + str(i) + '] = ((double) rand() / (RAND_MAX)) * ' + str(float(d_max) - float(d_min)) + ' + ' + d_min + ';\n')
    else:
        if nlparam[i].startswith('k_intra'):
            ff.write('      x0[' + str(i) + '] = ((double) rand() / (RAND_MAX)) * ' + str(float(k_max_intra) - float(k_min_intra)) + ' + ' + k_min_intra + ';\n')
        else:
            ff.write('      x0[' + str(i) + '] = ((double) rand() / (RAND_MAX)) * ' + str(float(k_max) - float(k_min)) + ' + ' + k_min + ';\n')

            
a = """
      

    model.set_nonlinear_parameters(x0);

    #   ifdef RIDGE_REGRESSION
    std::cout << "<> using ridge regression with alpha = "
              << alpha << std::endl;
#   endif

    std::cout << "\\n<><><> model type = '" << model.name() << "'\\n";

    {
        const char fn[] = "fit-2b-initial.cdl";
        std::ofstream ofs(fn);
        std::cout << "\\n>> dumping initial model as '" << fn << "' >>\\n\\n";
        model.as_cdl(ofs);
    }

    ++argv;

    try {
        while (--argc != 0) {
            size_t nd = tset::load_dimers(*argv, training_set);
            std::cout << "'" << *(argv++) << "' : "
                      << nd << " dimers" << std::endl;
        }
    } catch (const std::exception& e) {
        std::cerr << " ** Error ** : " << e.what() << std::endl;
        return 1;
    }

    //
    // assign weights
    //

    ts_weights = new double[training_set.size()];

    double E_min;
    size_t N_eff;

    tset::setup_weights(training_set, E_range, E_min,
                       ts_weights, N_eff, true);

    std::cout << "\\n>>   E_min = " << E_min << " kcal/mol"
                 "\\n>> E_range = " << E_range << " kcal/mol"
                 "\\n\\n>> training set size = " << training_set.size()
              << "\\n>>    effective size = " << N_eff << '\\n'
              << std::endl;


    // electrostatics
    double tb_ref[training_set.size()];
    for (size_t n = 0; n < training_set.size(); n++) {
      // Saving reference 2b energies  
      tb_ref[n] = training_set[n].energy_twobody ;

      x::mon1 m1(training_set[n].xyz);
      x::mon2 m2(training_set[n].xyz + 3*m1.get_nsites());

      int system_nsites = m1.get_nsites() + m2.get_nsites();
      double* system_sitecrds;
      double* system_charge;
      double* system_polfac;
      double* system_pol;

     system_sitecrds = new double [system_nsites*3];
      system_charge = new double [system_nsites];
      system_polfac = new double [system_nsites];
      system_pol = new double [system_nsites]; //allocates memory to the pointers

      std::copy(m1.get_sitecrds(), m1.get_sitecrds() + 3 * m1.get_nsites(),
                system_sitecrds);
      std::copy(m2.get_sitecrds(), m2.get_sitecrds() + 3 * m2.get_nsites(),
                system_sitecrds + 3 * m1.get_nsites());

      std::copy(m1.get_charges(), m1.get_charges() + m1.get_nsites(),
                system_charge);
      std::copy(m2.get_charges(), m2.get_charges() + m2.get_nsites(),
                system_charge + m1.get_nsites());

      std::copy(m1.get_pol(), m1.get_pol() + m1.get_nsites(),
                system_pol);
      std::copy(m2.get_pol(), m2.get_pol() + m2.get_nsites(),
                system_pol + m1.get_nsites());

      std::copy(m1.get_polfacs(), m1.get_polfacs() + m1.get_nsites(),
                system_polfac);
      std::copy(m2.get_polfacs(), m2.get_polfacs() + m2.get_nsites(),
                system_polfac + m1.get_nsites());


      excluded_set_type exclude12;
      excluded_set_type exclude13;
      excluded_set_type exclude14;

      for (auto i = m1.get_begin_12(); i != m1.get_end_12(); i++) {
        exclude12.insert(*i);
      }
      for (auto i = m2.get_begin_12(); i != m2.get_end_12(); i++) {
        std::pair<size_t,size_t> p =
                      std::make_pair(i->first + m1.get_nsites() ,
                                     i->second + m1.get_nsites());
        exclude12.insert(p);
      }

      for (auto i = m1.get_begin_13(); i != m1.get_end_13(); i++) {
        exclude13.insert(*i);
      }
      for (auto i = m2.get_begin_13(); i != m2.get_end_13(); i++) {
        std::pair<size_t,size_t> p =
                      std::make_pair(i->first + m1.get_nsites() ,
                                     i->second + m1.get_nsites());
        exclude13.insert(p);
      }

      for (auto i = m1.get_begin_14(); i != m1.get_end_14(); i++) {
        exclude14.insert(*i);
      }
      for (auto i = m2.get_begin_14(); i != m2.get_end_14(); i++) {
        std::pair<size_t,size_t> p =
                      std::make_pair(i->first + m1.get_nsites() ,
                                     i->second + m1.get_nsites());
        exclude14.insert(p);
      }

      ttm::electrostatics m_electrostatics;

      ttm::smear_ttm4x smr; // smearing for chloride?
      smr.m_aDD_intra_12 = 0.3;
      smr.m_aDD_intra_13 = 0.3;
  // Missing 14. Add it later.

      double ener = m_electrostatics(system_nsites, system_charge, system_polfac, system_pol,
                                    system_sitecrds, exclude12, exclude13, smr, 0);

      // Take out electrostatic energy:
      elec_e.push_back(ener);
      training_set[n].energy_twobody -= ener;
      // std::cerr << "Conf " << n << " : Elec= " << ener ;

      // Now need to take out dispersion
      x2b_disp disp(m1.get_sitecrds(), m2.get_sitecrds(), m1.get_nsites(), m2.get_nsites());
      ener = disp.get_dispersion();
      disp_e.push_back(ener);
      training_set[n].energy_twobody -= ener ;

      // std::cerr << " , Disp= " << ener << std::endl;
      delete[] system_sitecrds ;
      delete[] system_charge  ;
      delete[] system_polfac  ;
      delete[] system_pol ;

    }

        linear::allocate();

    gsl_vector* x = gsl_vector_alloc(model.get_num_nonlinear_params());
    model.get_nonlinear_parameters(x->data);

    gsl_multimin_function chisq_func;

    chisq_func.n = model.get_num_nonlinear_params();
    chisq_func.f = linear::compute_chisq;

    gsl_vector* ss = gsl_vector_alloc(model.get_num_nonlinear_params());
    gsl_vector_set_all(ss, 0.1);

    std::cout << "\\n<> initial simplex sides:\\n";
    for (size_t n = 0; n < model.get_num_nonlinear_params(); ++n)
        std::cout << n << " : " << ss->data[n] << "\\n";

    gsl_multimin_fminimizer* s =
        gsl_multimin_fminimizer_alloc(gsl_multimin_fminimizer_nmsimplex2rand,
                                      model.get_num_nonlinear_params());

    gsl_multimin_fminimizer_set(s, &chisq_func, x, ss);

    int iter(0), status(0);
    //
    // Main optimization loop
    //

    do {
        ++iter;
        status = gsl_multimin_fminimizer_iterate(s);

        if (status)
             break;

        const double size = gsl_multimin_fminimizer_size(s);
        status = gsl_multimin_test_size(size, 1e-4);
        //status = gsl_multimin_test_size(size, 1e-3); //changed it to test convergence 

        if (status == GSL_SUCCESS)
            std::cout << "!!! converged !!!" << std::endl;

        std::cout << iter << ' ' << s->fval << ' ' << size << std::endl;
        if (iter > 0 && iter%10 == 0) {
            std::cout << "\\n<> solution:\\n";
            for (size_t n = 0; n <  model.get_num_nonlinear_params(); ++n)
                std::cout << n << " : " << s->x->data[n] << "\\n";
            std::cout << "<>" << std::endl;
        }
    } while (status == GSL_CONTINUE && iter < 5000);

    model.set_nonlinear_parameters(s->x->data);
    linear::compute_chisq(s->x, 0);
    model.set(linear::params);

    gsl_vector_free(x);
    gsl_vector_free(ss);
    gsl_multimin_fminimizer_free(s);

    //
    // report
    //

    for (size_t i = 0; i < training_set.size(); ++i)
      training_set[i].energy_twobody += elec_e[i] + disp_e[i];

    ofstream correlation_file;
    correlation_file.open ("correlation.dat");
    double err_L2(0), err_wL2(0), err_Linf(0);
    double err_L2_lo(0), err_Linf_lo(0), nlo(0);

    for (size_t i = 0; i < training_set.size(); ++i) {

        const double E_model = model(training_set[i].xyz) + elec_e[i] + disp_e[i];
        const double delta = E_model - training_set[i].energy_twobody;
        if (std::abs(delta) > err_Linf)
            err_Linf = std::abs(delta);

  correlation_file <<  i+1   << "   "
    << E_model  << "   "
    <<  training_set[i].energy_twobody  << "    "
          <<  delta*delta  << "    \\n" ;

        err_L2 += delta*delta;
        err_wL2 += ts_weights[i]*delta*delta;

        if (training_set[i].energy_total - E_min < E_range) {
            nlo += 1.0;
            err_L2_lo += delta*delta;
            if (std::abs(delta) > err_Linf_lo)
                err_Linf_lo = std::abs(delta);
        }
    }

    correlation_file.close();

    err_L2 /= training_set.size();
    err_wL2 /= training_set.size();

    err_L2_lo /= nlo;

    std::cout << "      err[L2] = " << std::sqrt(err_L2) << "    #rmsd of full ts\\n"
              << "     err[wL2] = " << std::sqrt(err_wL2) << "   #weighted rmsd of full ts\\n"
              << "    err[Linf] = " << err_Linf << "   #highest error in full ts\\n"
              << "  err[L2,low] = " << std::sqrt(err_L2_lo) << "   #rmsd of low-energy ts \\n"
              << "err[Linf,low] = " << err_Linf_lo << "   #highest error in low-energy ts "
              << std::endl;

    //
    //  save
    //

    {
        const char fn[] = "fit-2b.cdl";
        std::ofstream ofs(fn);
        std::cout << "\\n>> saving as '" << fn << "'\\n";
        model.as_cdl(ofs);
    }


    return 0;
}

"""
ff.write(a)
ff.close()


# ## Makefile

# In[306]:

fname = "Makefile"
ff = open(fname,'w')
a = """
CXX=g++
CXXFLAGS= -g -Wall -std=c++11 -O0 -m64 -I/opt/intel/mkl/include
LIBS = -lnetcdf -lgsl -lgslcblas -L/opt/intel/lib/intel64 -L/opt/intel/mkl/lib/intel64 -lmkl_intel_lp64 -lmkl_intel_thread -lmkl_core -liomp5 -lpthread

AR = /usr/bin/ar
OBJDIR = .
LIBDIR = ./
INCLUDE = -I./

FIT_OBJ = fit-utils.o coulomb.o electrostatics.o gammq.o io-xyz.o \\
kvstring.o mon1.o mon2.o ps.o rwlsq.o wlsq.o stuff.o tang-toennies.o \\
training_set.o ttm4.o wlsq.o poly_2b_""" + mon1 + """_""" + mon2 + """_v1x.o \\
x2b_""" + mon1 + """_""" + mon2 + """_v1x.o poly_2b_""" + mon1 + """_""" + mon2 + """_v1.o \\
dispersion.o poly_2b_""" + mon1 + """_""" + mon2 + """.o

all: libfit.a fit-2b
# $(MAKE) libpot.a 2> err.txt > log.txt


libfit.a: $(addprefix $(OBJDIR)/, $(FIT_OBJ))
\t$(AR) cru libfit.a $(addprefix $(OBJDIR)/, $(FIT_OBJ))

fit-2b: fit-2b.cpp
\t$(CXX) $(CXXFLAGS) $(INCLUDE) -L$(LIBDIR) $< $(LIBS) -lfit -o $@


$(OBJDIR)/%.o: %.cpp $(OBJDIR)/.sentinel
\t$(CXX) $(CXXFLAGS) $(INCLUDE) -L$(LIBDIR) -c $< $(LIBS) -o $@

$(OBJDIR)/.sentinel:
\tmkdir -p $(OBJDIR)
\ttouch $@

clean:
\trm -rf $(addprefix $(OBJDIR)/, $(FIT_OBJ)) libfit.a fit-2b
"""
ff.write(a)
ff.close()


# ## Poly_fit_header

# In[307]:

fname = "poly_2b_" + mon1 + "_" + mon2 + ".h"
ff = open(fname,'w')
a = """
#ifndef POLY_2B_""" + mon1 + "_" + mon2 + """_H
#define POLY_2B_""" + mon1 + "_" + mon2 + """_H

namespace mb_system_fit {

struct poly_model{
    static const unsigned degree = """ + str(degree) + """;
    static const unsigned n_vars = """ + str(nvars) + """;

    static const unsigned size = """ + str(npoly) + """;

    void eval(const double x[n_vars], double*);
};

} // namespace

#endif

"""
ff.write(a)
ff.close()


# ## Modifi poly-direct.cpp file to give just the non linear terms

# In[308]:

fdirect = open(directcpp, 'r')
fnamecpp = "poly_2b_" + mon1 + "_" + mon2 + ".cpp"
fpolycpp = open(fnamecpp,'w')
fnameh = "poly_2b_" + mon1 + "_" + mon2 + ".h"
a = """
#include \"""" + fnameh + """\"

namespace mb_system_fit {

void poly_model::eval(const double x[""" + str(nvars) + """], double a[""" + str(npoly) + """])
{
    double p[""" + str(npoly) + """];
    
    // Degree 1
"""
fpolycpp.write(a)

for line in fdirect.readlines():
    if line.startswith('    p['):
        fpolycpp.write(line)
    
a = """
for(int i = 0; i < """ + str(npoly) + """; ++i)
        a[i] = p[i];

}
} // namespace mb_system
"""

fpolycpp.write(a)
fpolycpp.close()





# In[ ]:



