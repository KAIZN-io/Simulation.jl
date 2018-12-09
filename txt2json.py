import json
import re
import os
exec(open("SYSTEM/py_packages.py").read())


cwd = os.getcwd()

model = 'ion'

system_comp = ['copa','equation','ODE']
dict_system = {}

system_comp_remove = []

"""pre-check whether the system_comp exists for the specific model"""
for system in system_comp:
    if os.path.isfile('{0}/Single_Models/{1}/{1}_{2}.txt'.format(cwd,model,system)) == False:
        system_comp_remove.append(system)
for i in system_comp_remove:
    system_comp.remove(i)


for system in system_comp:
    f = open('{0}/Single_Models/{1}/{1}_{2}.txt'.format(cwd, model,system))

    string_list = [line for line in f]

    dict_spec = {}

    if system == 'copa':
        try:
            # .strip() removes leading and ending whitespaces
            for string_line in range(len(string_list)):
                key = string_list[string_line][string_list[string_line].find(""):string_list[string_line].find("=")].strip()
                value = string_list[string_line][string_list[string_line].find("=")+1:string_list[string_line].find("\n")]
                dict_spec[key] = value

            dict_system[system] = dict_spec
        except FileNotFoundError:
            pass
    else:
        dict_system[system] = dict_spec
        for string_line in range(len(string_list)):

            """
            remove whitespaces and split the string
            QUESTION: is the replacing realy nessesary?
            """
            split_equation = string_list[string_line].replace("", " ").replace('=',' ').replace('-',' ').split()

            """.strip() removes leading and ending whitespaces"""
            key = string_list[string_line][string_list[string_line].find(""):string_list[string_line].find("=")].strip()
            value = string_list[string_line][string_list[string_line].find("=")+1:string_list[string_line].find("\n")]

            """split the value string"""
            dict_spec[key] = {}
            dict_spec[key]['component'] = {}
            splitted = value.split()

            

            """step 1 : "dont touch that"""
            parenthese_open = 0
            parenthese_close = 0
            join_str_list = []
            join_if = []

            beginning = -1
            ending = -1
            for j,i in enumerate(splitted):
                if '(' in i:
                    parenthese_open += i.count('(')

                    if beginning < 0:
                        beginning = j

                if ')' in i:
                    parenthese_close += i.count(')')

                    if (parenthese_open == parenthese_close) and parenthese_open > 0:

                        ending = j
                        join_str_list.append([beginning,ending])

                        beginning = -1
                        ending = -1
                        parenthese_open = 0
                        parenthese_close = 0

                if ('if' in i) and len(i)==2:
                    join_if.append(j)

            for k in join_if:
                dict_spec[key]['condition'] = ' '.join(splitted[k::])
                del splitted[k::]


            """invert the list iteration --> then join the pieces together"""
            for i in join_str_list[::-1]:
                a = ''.join(splitted[i[0]:i[1]+1])

                del splitted[i[0]:i[1]+1]
                splitted.insert(i[0],a)

            """step 2 : create the "component" for the variable"""
            join_marker = [0]

            term_separator = ['+','-']
            for i,j in enumerate(splitted):
                if j in term_separator:
                    join_marker.append(i)


            join_marker.insert(len(join_marker),len(splitted))

            dict_spec[key]['component'] = {}
            """next step: remove the differential d"""
            if key[0] == 'd':
                key_surrogate = key[1:]
            else:
                key_surrogate = key
            for i in range(len(join_marker)-1):
                a = ''.join(splitted[join_marker[i]:join_marker[i+1]])

                dict_spec[key]['component']['pat{}{}'.format(key_surrogate,i+1)] = a

           
            """last step: remove keys without values --> remove zombies"""
            keys_to_delete = []
            for remove_key, value in dict_spec[key]['component'].items():
                if value == "":
                    keys_to_delete.append(remove_key)
            for remove_key in keys_to_delete:
                dict_spec[key]['component'].pop(remove_key, None)

        """sql to json 
        
        get the corresponding units of the variables(keys)
        """
        if system == 'ODE':
            pass
 

         

if model == 'hog':

    hog_stimulus = {}
    hog_stimulus['copa'] = dict_system['copa']
    hog_stimulus['equation'] = {}
    hog_stimulus['equation']['NaCl'] = {'component':{'patNaCl1' : "(0 if t < t0 else single_impuls_NaCl) if signal_type == 1 else ((single_impuls_NaCl if (t0 <= t and t < (t0 + t1)) else 0) if signal_type == 2 else ((single_impuls_NaCl if ((t - t0 - math.floor((t - t0) / (t1 + t2)) * (t1 + t2)) <= t1) else 0) if signal_type == 3 else ((max_NaCl if (0 if t < t0 else single_impuls_NaCl * math.ceil((t - t0) / t1)) > max_NaCl else (0 if t < t0 else single_impuls_NaCl * math.ceil((t - t0) / t1))) if signal_type == 4 else 0)))"}}
    hog_stimulus['ODE'] = dict_system['ODE']

    for key,value in dict_system['equation'].items():
        hog_stimulus['equation'][key] = value

    dict_system = hog_stimulus



"""create json format"""

s = json.dumps(dict_system, indent=4)
with open('{0}/Single_Models/json_files/{1}_system.json'.format(cwd, model),"w") as f:
    f.write(s)


# exec(open('{0}/Single_Models/{1}/{1}.py'.format(cwd, model),encoding="utf-8").read())
