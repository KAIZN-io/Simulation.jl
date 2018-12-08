dL_ArH = k_incrArH - k_decrArH * L_ArH if t >= t0_glucose and t < t1_glucose and Glucose == True else 0
dL_HH = k_incrHH - k_decrHH * L_HH if t >= t0_glucose and t < t1_glucose and Glucose == True else 0
dATP = k_ATPincr - k_ATPdecr * ATP if t >= t0_glucose and ATP < 2.5 and Glucose == True else 0
dH_out = (J_H * Surf) / V_out
dK_out = (J_K * Surf) / V_out
dNa_out = (J_Na * Surf) / V_out
dCl_out = (J_Cl * Surf) / V_out
dH_in = - (J_H * Surf * np.log(10) * H_in)/(V_in * pbc)
dK_in = - (J_K * Surf) / V_in
dNa_in = - (J_Na * Surf) / V_in
dCl_in = - (J_Cl * Surf) / V_in
dDeltaphi = - (2 * F / C_m) * (J_H + J_K + J_Na - J_Cl)
