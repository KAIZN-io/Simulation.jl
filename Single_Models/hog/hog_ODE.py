dGlyc_in = k_s0Glyc + ((k_s1Glyc * totalHog1PP ** 4) / (beta ** 4 + totalHog1PP ** 4)) + k_s2Glyc * Yt - (k_exp0Glyc + ((k_exp1Glyc * PI_t ** hill_exponent_eflux) / (gamma ** hill_exponent_eflux + PI_t ** hill_exponent_eflux))) * (Glyc_in - Glyc_ex) - Glyc_in * V_ratio
dHog1PPc = k_phoHog1 * Pbs2PP * Hog1c - k_dephoHog1PPc * Hog1PPc - k_impHog1PPc * Hog1PPc + ((k_expHog1PPn * Hog1PPn * V_nuc) / V_cyt) - Hog1PPc * V_ratio
dHog1PPn = ((k_impHog1PPc * Hog1PPc * V_cyt) / V_nuc) - k_expHog1PPn * Hog1PPn - k_dephoHog1PPn * Hog1PPn - Hog1PPn * V_ratio
dHog1c = - k_phoHog1 * Pbs2PP * Hog1c + k_dephoHog1PPc * Hog1PPc - k_impHog1c * Hog1c + ((k_expHog1n * Hog1n * V_nuc) / V_cyt) - Hog1c * V_ratio
dHog1n = ((k_impHog1c * Hog1c * V_cyt) / V_nuc) - k_expHog1n * Hog1n + k_dephoHog1PPn * Hog1PPn - Hog1n * V_ratio
dPbs2 = -((k_phoPbs2 * Pbs2) / (1 + (PI_t / alpha) ** hill_exponent)) + k_dephoPbs2 * Pbs2PP - Pbs2 * V_ratio
dPbs2PP = ((k_phoPbs2 * Pbs2) / (1 + (PI_t / alpha) ** hill_exponent)) - k_dephoPbs2 * Pbs2PP - Pbs2PP * V_ratio
dV_os = - G * Lp * (PI_e + PI_t - PI_i)
dYt = k_s0Yt + k_s1Yt * z4 - k_tYt * Yt - Yt * V_ratio
dz1 = ((4 * (Hog1PPn - z1)) / tau)
dz2 = ((4 * (z1 - z2)) / tau)
dz3 = ((4 * (z2 - z3)) / tau)
dz4 = ((4 * (z3 - z4)) / tau)