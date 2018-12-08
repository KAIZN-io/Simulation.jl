dL_ArH = k_incrArH - k_decrArH * L_ArH if t >= t0_glucose and t < t1_glucose and Glucose == True else 0
dL_HH = k_incrHH - k_decrHH * L_HH if t >= t0_glucose and t < t1_glucose and Glucose == True else 0
dATP = k_ATPincr - k_ATPdecr * ATP if t >= t0_glucose and ATP < 2.5 and Glucose == True else 0
dDeltaphi = - (2 * F / C_m) * (J_H + J_K + J_Na - J_Cl)
dPbs2 = -((k_phoPbs2 * Pbs2) / (1 + (pi_t / alpha) ** hill_exponent)) + k_dephoPbs2 * Pbs2PP - Pbs2 * V_ratio
dPbs2PP = ((k_phoPbs2 * Pbs2) / (1 + (pi_t / alpha) ** hill_exponent)) - k_dephoPbs2 * Pbs2PP - Pbs2PP * V_ratio
dHog1c = - k_phoHog1 * Pbs2PP * Hog1c + k_dephoHog1PPc * Hog1PPc - k_impHog1c * Hog1c + ((k_expHog1n * Hog1n * V_nuc) / V_cyt) - Hog1c * V_ratio
dHog1PPc = k_phoHog1 * Pbs2PP * Hog1c - k_dephoHog1PPc * Hog1PPc - k_impHog1PPc * Hog1PPc + ((k_expHog1PPn * Hog1PPn * V_nuc) / V_cyt) - Hog1PPc * V_ratio
dHog1n = ((k_impHog1c * Hog1c * V_cyt) / V_nuc) - k_expHog1n * Hog1n + k_dephoHog1PPn * Hog1PPn - Hog1n * V_ratio
dHog1PPn = ((k_impHog1PPc * Hog1PPc * V_cyt) / V_nuc) - k_expHog1PPn * Hog1PPn - k_dephoHog1PPn * Hog1PPn - Hog1PPn * V_ratio
dGlyc_in = k_s0Glyc + ((k_s1Glyc * totalHog1PP ** 4) / (beta ** 4 + totalHog1PP ** 4)) + k_s2Glyc * Yt - (k_exp0Glyc + ((k_exp1Glyc * pi_t ** hill_exponent_eflux) / (gamma ** hill_exponent_eflux + pi_t ** hill_exponent_eflux))) * (Glyc_in - Glyc_ex) - Glyc_in * V_ratio
dYt = k_s0Yt + k_s1Yt * z4 - k_tYt * Yt - Yt * V_ratio
dz1 = ((4 * (Hog1PPn - z1)) / tau)
dz2 = ((4 * (z1 - z2)) / tau)
dz3 = ((4 * (z2 - z3)) / tau)
dz4 = ((4 * (z3 - z4)) / tau)
dpi_t = (E * 2 * d / (1 - nu) * (rdt / ( r ** 2) - R_refdt / (R_ref * r)) - rdt / r * pi_t)
dR_ref = R_refdt
dr_os = r_osdt
dr_b = r_bdt
dr = rdt
dc_i =  Na_indt  + K_indt + Cl_indt + H_indt + dGlyc_in
dH_in = H_indt
dCl_in = Cl_indt
dCl_out = Cl_outdt
dH_out = H_outdt
dK_in = K_indt
dK_out = K_outdt
dNa_in = Na_indt
dNa_out = Na_outdt