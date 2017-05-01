""""
    Plots figure 6: energy time series, budgets,
                    wave-vorticity correlation
                    for varying dispersivities.
"""

import h5py
import numpy as np
import matplotlib.pyplot as plt

from Utils import *

plt.close('all')

#path = "outputs/decaying_turbulence/coupled_new/Uw10/lambdaz"
path = "outputs/decaying_turbulence/parameter_exploration_new/Uw0.1/lambdaz"
patho = "../writeup/figs/"

#for lambdaz in [198.75, 400.0]:
for lambdaz in [562.149891043]:
#for lambdaz in [281.074945522, 397.5]:

    pathi = path+str(lambdaz)+"/"
    params = h5py.File(pathi+"parameters.h5","r")
    diags = h5py.File(pathi+"diagnostics.h5")

    ## get params
    Ue, ke = params['dimensional/Ue'][()], params['dimensional/ke'][()]
    Te = params['dimensional/Te'][()]
    Uw = params['dimensional/Uw'][()]

    ## get diagnostics
    time = diags['time'][:]
    KE_qg = diags['ke_qg'][:]
    PE_niw = diags['pe_niw'][:]
    KE_niw = diags['ke_niw'][:]
    ENS_qg = diags['ens'][:]
    g1 = diags['gamma_r'][:]
    g2 = diags['gamma_a'][:]
    pi = diags['pi'][:]
    cKE_niw = diags['cke_niw'][:]
    iKE_niw = diags['ike_niw'][:]
    ep_phi = diags['ep_phi'][:]
    ep_psi = diags['ep_psi'][:]
    chi_q =  diags['chi_q'][:]
    chi_phi =  diags['chi_phi'][:]
    conc_niw =  diags['conc_niw'][:]
    skew =  diags['skew'][:]

    ## calculate tendency from energy time series
    dt = time[1]-time[0]
    dPE = np.gradient(PE_niw,dt)
    dKE = np.gradient(KE_qg,dt)
    diKE_niw = np.gradient(iKE_niw,dt)

    res_ke = dKE-(-g1-g2+ep_psi)
    res_pe = dPE-g1-g2-chi_phi

    # arrays
    try:
        dKe = np.concatenate([dKe, (KE_qg[...,np.newaxis]-KE_qg[0])/KE_qg[0]],axis=1)
        dPw = np.concatenate([dPw, (PE_niw[...,np.newaxis]-PE_niw[0])/KE_qg[0]],axis=1)
        hslash = np.hstack([hslash, params['nondimensional/hslash'][()]])
        Conc = np.concatenate([Conc, conc_niw[...,np.newaxis]],axis=1)
        Skew = np.concatenate([Skew, skew[...,np.newaxis]],axis=1)
        G1 = np.concatenate([G1, g1[...,np.newaxis]],axis=1)
        G2 = np.concatenate([G2, g2[...,np.newaxis]],axis=1)
        CHI_PHI = np.concatenate([CHI_PHI, chi_phi[...,np.newaxis]],axis=1)
        EP_PHI = np.concatenate([EP_PHI, ep_phi[...,np.newaxis]],axis=1)
    except:
        dKe = (KE_qg[...,np.newaxis]-KE_qg[0])/KE_qg[0]
        dPw = (PE_niw[...,np.newaxis]-PE_niw[0])/KE_qg[0]
        hslash = np.array(params['nondimensional/hslash'][()])
        Conc = conc_niw[...,np.newaxis]
        Skew = skew[...,np.newaxis]
        G1 = g1[...,np.newaxis]
        G2 = g2[...,np.newaxis]
        CHI_PHI = chi_phi[...,np.newaxis]
        EP_PHI = ep_phi[...,np.newaxis]

# ## plotting
fig = plt.figure(figsize=(8.5,6.))
lw, alp = 3.,.5
KE0 = KE_qg[0]
tmax = time[-1]

ax = fig.add_subplot(221)

for i in range(hslash.size):
    p = plt.plot(time/Te,dPw[:,i],label="$\hslash = $"+str(round(hslash[i]*100)/100),\
                    linewidth=lw,alpha=alp)
    color = p[0].get_color()
    plt.plot(time/Te,dKe[:,i],'--',color=color,linewidth=lw,alpha=alp)

plt.xticks([])
plt.ylim(-0.45,0.45)
plt.ylabel(r'Energy  change $[(E-E_0) \times {2}/{U_e^2} ]$')
plt.legend(loc=(0.4,1.1),ncol=5)
plt.plot([0,tmax/Te],[0]*2,'--',color="0.5")
fig.subplots_adjust(wspace=.4)
plot_fig_label(ax, label="a")

#
ax = fig.add_subplot(222)

plt.xticks([])
#plt.ylim(-0.005,0.0125)
plt.plot([0,tmax/Te],[0]*2,'--',color="0.5")
plt.plot(time/Te,Conc,label=r'$\Pi$',linewidth=lw,alpha=alp)
plt.ylabel(r"Wave-vorticity correlation [r]")
plot_fig_label(ax, label="b")

ax = fig.add_subplot(223)
plt.plot(time/Te,Te*G1/KE_qg[0],label=r'$\Pi$',linewidth=lw,alpha=alp)
#plt.ylim(-0.005,0.0125)
plt.plot([0,tmax/Te],[0]*2,'--',color="0.5")
plt.ylabel(r'Power $[\Gamma_r \times {2 k_e}/{U_e} ]$')
plot_fig_label(ax, label="c")
plt.xlabel(r"Time [$t \times U_e k_e$]")

ax = fig.add_subplot(224)
plt.plot(time/Te,Te*G2/KE_qg[0],label=r'$\Pi$',linewidth=lw,alpha=alp)
plt.plot([0,tmax/Te],[0]*2,'--',color="0.5")
plt.ylabel(r'Power $[\Gamma_a \times {2 k_e}/{U_e} ]$')
plot_fig_label(ax, label="d")
plt.xlabel(r"Time [$t \times U_e k_e$]")
plt.savefig(patho+"fig5.pdf", bbox_inches='tight')


#
# ax = fig.add_subplot(223)
# plt.plot(time/Te,Te*pi/KE0,label=r'$\Pi$',linewidth=lw,alpha=alp)
# plt.plot(time/Te,Te*ep_psi/KE0,label=r'$\epsilon_\phi$',linewidth=lw,alpha=alp)
# plt.plot(time/Te,Te*(pi+ep_phi)/KE0,label=r'$\Pi+\epsilon_\phi$',linewidth=lw,alpha=alp)
# plt.plot(time/Te,Te*diKE_niw/KE0,'k--',label=r'$\dot K_w^i$'
#                 ,linewidth=lw,alpha=alp)
# plt.xlabel(r"Time [$t \times U_e k_e$]")
# plt.ylabel(r'Power $[\dot E \times {2 k_e}/{U_e} ]$')
# plt.legend(loc=1,ncol=2)
# plot_fig_label(ax, label="c")
#
# fig.subplots_adjust(hspace=.125)
#
# ax = fig.add_subplot(224)
# p1 = ax.plot(time/Te,conc_niw,linewidth=lw,alpha=alp,label='NIW concentration, $C$')
# plt.ylabel(r"Wave-vorticity correlation [r]")
# plt.xlabel(r"Time [$t \times U_e k_e$]")
# plt.plot([0,tmax/Te],[0]*2,'--',color="0.5")
# plt.ylim(-0.8,0.3)
# plot_fig_label(ax, label="d")

#plt.savefig(patho+"fig5.pdf", bbox_inches='tight')
