# in copy past file
# TODO: schaffe diese Codezeilen auch noch aus die def hog_model()
signal_type = dict_stimulus.get('signal_type')[0]

single_impuls_NaCl = dict_stimulus.get('NaCl_impuls')[0]

t0 = dict_time.get('NaCl_impuls_start')

t1 = t0 / 2 if signal_type == 3 else t0 + 300
t2 = t0 / 2 if signal_type == 3 else 1

if signal_type == 1:
    NaCl = 0 if t < t0 else single_impuls_NaCl

if signal_type == 2:
    NaCl = single_impuls_NaCl if (t0 <= t and t < (t0 + t1)) else 0

if signal_type == 3:
    NaCl = single_impuls_NaCl if ((t - t0 - math.floor((t - t0) / (t1 + t2)) * (t1 + t2)) <= t1) else 0

if signal_type == 4:
    NaCl = 0 if t < t0 else single_impuls_NaCl * math.ceil((t - t0) / t1)
    NaCl = max_NaCl if NaCl > max_NaCl else NaCl

# in json file (with NaCl)
V_cell = V_os + V_b
V_cyt = 0.5 * V_cell
V_nuc = 0.07 * V_cell
PI_e = PI_e0 + w * NaCl
PI_t = max(PI_t0 * (V_os - V_osPIt) / (V_os0 - V_osPIt), 0)
PI_i = ((n_0 + Glyc_in * V_cyt) / V_os) * R * T
V_ratio = -G * Lp * (PI_e + PI_t - PI_i) / V_cell
n_totalHog1 = (Hog1c * V_cyt + Hog1n * V_nuc + Hog1PPc * V_cyt + Hog1PPn * V_nuc)
totalHog1PP = (Hog1PPc * V_cyt + Hog1PPn * V_nuc) * 602 / 6780
