dR_ref = R_refdt
dc_i = (k_uptake * G - k_consumption * V * (10 ** 15))
dpi_t = E * 2 * d / (1 - nu) * (rdt / r ** 2 - R_refdt / (R_ref * r)) - rdt / r * pi_t
dr = rdt
dr_os = r_osdt
dr_b = r_bdt
