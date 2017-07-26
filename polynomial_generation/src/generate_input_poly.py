
# coding: utf-8

# In[1]:

import sys
import os


# In[2]:

if len(sys.argv) != 2:
    print("Usage: ./script <input>")
    print("input must be in the form of A1B2_A1B2, A1_B2, ...")
    print("The script will create a file named input.in, e.g. A1B2_A1B2.in")
    print("If the molecule has virtual sites, such as lone pairs, use the letter Z")
    sys.exit()
else:
    molec = sys.argv[1]


# In[8]:

f = open(molec+".in", 'w')
mon1 = molec.split('_')[0]
mon2 = molec.split('_')[1]
f.write('add_molecule[\'' + mon1 + '\']\n')
f.write('add_molecule[\'' + mon2 + '\']\n')
vsites = ['Z','Y','X']


# In[9]:

types_a = list(mon1)
types_b = list(mon2)


# In[10]:

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


# In[11]:

nc = 0
set_m1 = []
set_m2 = []
for i in range(0,len(types_a),2):
    n = 1
    if (int(types_a[i+1]) == 1):
        if not types_a[i] in vsites:
            set_m1.append(types_a[i] + '_' +  '_a')
    else:
        for j in range(int(types_a[i+1])):
            if not types_a[i] in vsites:
                set_m1.append(types_a[i] + '_' + str(n) + '_a')
                n = n + 1
                nc = nc + 1

for i in range(0,len(types_b),2):
    n = 1
    if (int(types_b[i+1]) == 1):
        if not types_b[i] in vsites:
            set_m2.append(types_b[i] + '_' +  '_b')
    else:
        for j in range(int(types_b[i+1])):
            if not types_b[i] in vsites:
                set_m2.append(types_b[i] + '_' + str(n) + '_b')
                n = n + 1
                nc = nc + 1
            
for i in range(0,len(types_a),2):
    n = 1
    for j in range(int(types_a[i+1])):
        if types_a[i] in vsites:
            set_m1.append(types_a[i] + '_' + str(n) + '_a')
            n = n + 1

for i in range(0,len(types_b),2):
    n = 1
    for j in range(int(types_b[i+1])):
        if types_b[i] in vsites:
            set_m2.append(types_b[i] + '_' + str(n) + '_b')
            n = n + 1


# In[12]:

f.write('\n')
# Intramolecular distances:
for i in range(0,len(set_m1) - 1):
    for j in range(i + 1,len(set_m1)):
        ti = set_m1[i].split('_')
        tj = set_m1[j].split('_')
        t = ''.join(sorted(ti[0] + tj[0]))
        if not ti[0] in vsites and not tj[0] in vsites:
            f.write('add_variable[\'' + ti[0] + ti[1] + '\', \'' + ti[2] + '\', \''                   + tj[0] + tj[1] + '\', \'' + tj[2] + '\', \'x-intra-' + t + '\']\n')
            
for i in range(0,len(set_m2) - 1):
    for j in range(i + 1,len(set_m2)):
        ti = set_m2[i].split('_')
        tj = set_m2[j].split('_')
        t = ''.join(sorted(ti[0] + tj[0]))
        if not ti[0] in vsites and not tj[0] in vsites:
            f.write('add_variable[\'' + ti[0] + ti[1] + '\', \'' + ti[2] + '\', \''                   + tj[0] + tj[1] + '\', \'' + tj[2] + '\', \'x-intra-' + t + '\']\n')
# Intermolecular distances
for i in range(0,len(set_m1)):
    for j in range(0,len(set_m2)):
        ti = set_m1[i].split('_')
        tj = set_m2[j].split('_')
        t = ''.join(sorted(ti[0] + tj[0]))
        f.write('add_variable[\'' + ti[0] + ti[1] + '\', \'' + ti[2] + '\', \''                   + tj[0] + tj[1] + '\', \'' + tj[2] + '\', \'x-' + t + '\']\n')
f.close()


# In[ ]:



