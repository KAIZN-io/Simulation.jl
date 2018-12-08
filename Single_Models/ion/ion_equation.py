A_Ar = (R*T/(c_strich_ATP)) * (ATP - c_strich_ATP) * (1 + K_eq)
J_H = R*T*(L_HH * np.log(H_in / H_out) + L_HK * np.log(K_in / K_out) + L_HNa * np.log(Na_in / Na_out) + L_HCl * np.log(Cl_in / Cl_out)) + F * Deltaphi * (L_HH + L_HK + L_HNa - L_HCl) - L_ArH * A_Ar
J_K = R*T*(L_KH * np.log(H_in / H_out) + L_KK * np.log(K_in / K_out)) + F * Deltaphi * (L_KH + L_KK)
J_Na = R*T*(L_NaH * np.log(H_in / H_out) + L_NaNa * np.log(Na_in / Na_out)) + F * Deltaphi * (L_NaH + L_NaNa)
J_Cl = R*T*(L_ClH * np.log(H_in / H_out) + L_ClCl * np.log(Cl_in / Cl_out)) + F * Deltaphi * (L_ClH - L_ClCl)
