# copy past
# algebraic equations
t0_glucose = dict_time.get('Glucose_impuls_start')
t1_glucose = dict_time.get('Glucose_impuls_end')

Glucose = switch[0]

# in json file
V_cell = 4/3 * np.pi * r**3
G = 4 * np.pi * r ** 2

# V_cyt and V_nuc are assumed to be proportional to the cell volume V
V_cyt = 0.5 * V_cell
V_nuc = 0.07 * V_cell
V_os = 4/3 * np.pi * r**3 - 4/3 * np.pi * r_b**3

A_Ar = (R*T/(c_strich_ATP)) * (ATP - c_strich_ATP) * (1 + K_eq)

# fluxes over membrane
J_H = R*T*(L_HH * np.log(H_in / H_out) + L_HK * np.log(K_in / K_out) + L_HNa * np.log(
    Na_in / Na_out) + L_HCl * np.log(Cl_in / Cl_out)) + F * Deltaphi * (
                  L_HH + L_HK + L_HNa - L_HCl) - L_ArH * A_Ar
J_K = R*T*(L_KH * np.log(H_in / H_out) + L_KK * np.log(K_in / K_out)) + F * Deltaphi * (
                  L_KH + L_KK)
J_Na = R*T*(L_NaH * np.log(H_in / H_out) + L_NaNa * np.log(
    Na_in / Na_out)) + F * Deltaphi * (L_NaH + L_NaNa)
J_Cl = R*T*(L_ClH * np.log(H_in / H_out) + L_ClCl * np.log(Cl_in / Cl_out)) + F * Deltaphi * (
                   L_ClH - L_ClCl)

Na_indt = - (J_Na * G) / V_cell
Cl_indt = - (J_Cl * G) / V_cell
K_indt = - (J_K * G) / V_cell
H_indt = - (J_H * G * np.log(10) * H_in)/(V_cell * pbc)

Na_outdt = (J_Na * G) / V_out
Cl_outdt = (J_Cl * G) / V_out
K_outdt = (J_K * G) / V_out
H_outdt = (J_H * G) / V_out

c_e = H_out + K_out + Cl_out + Na_out + c_ext_extra

# pressure
pi_e = c_e * R * T
pi_i = c_i * R * T
#pi_i = ((Glyc_in * V_cyt) / V_os) * R * T + c_i * R * T - Glyc_in * R * T

V_ratio = - G * Lp * (pi_e + pi_t - pi_i) / (V_cell)

R_ref = r / (1 + (1 - nu) * (pi_t * r) / (E * 2 * d))     # relaxed cell radius
V_ref = 4 / 3 * np.pi * R_ref ** 3                        # relaxed cell volume
#V_ref = 4 / 3 * np.pi * 10 **(-15) * R_ref ** 3          # relaxed cell volume

# pi_c gibt den Endwert der Relaxation des Turgor Druckes an
# wenn pi_c und pi_t gleich, dann ist die Zelle entspannt --> R_refdt = 0
R_refdt = phi * R_ref * r / (2 * d) * max(pi_t - pi_c, 0)   # change relaxed cell radius

r_osdt = - Lp * (pi_t + pi_e - pi_i)
r_bdt = 0.2 * R_refdt
rdt = r_bdt + r_osdt


n_totalHog1 = (Hog1c * V_cyt + Hog1n * V_nuc + Hog1PPc * V_cyt + Hog1PPn * V_nuc)
totalHog1PP = (Hog1PPc * V_cyt + Hog1PPn * V_nuc) / n_totalHog1
