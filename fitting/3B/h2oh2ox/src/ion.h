#include "molecule.h"

namespace ion {
   
   class ion      : public molecule {
      
   public : 
       ion();
       ~ion();

       ion(double* crd);

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
       excluded_set_type::iterator get_end_12();
       excluded_set_type::iterator get_end_13();

   };

} //namespace ion

