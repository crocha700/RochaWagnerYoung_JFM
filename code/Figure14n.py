""""
    Plots figure sinxsiny: energy time series, budgets,
                    wave-vorticity correlation
                    of the decaying macroturbulence solution.
"""

import h5py
import numpy as np
import matplotlib.pyplot as plt

from Utils import *

plt.close('all')

pathi = "outputs/sinxsiny/"

patho = "../writeup/figs/"

params = h5py.File(pathi+"parameters.h5","r")
diags = h5py.File(pathi+"diagnostics.h5")

## get params
Ue, ke = params['dimensional/Ue'][()], params['dimensional/ke'][()]
Te = params['dimensional/Te'][()]
Uw = params['dimensional/Uw'][()]

alpha = params['nondimensional/alpha'][()]
hslash = params['nondimensional/hslash'][()]


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

## plotting
fig = plt.figure(figsize=(8.5,4))
lw, alp = 2.,1.
KE0 = KE_qg[0]
tmax = time[-1]

ax = fig.add_subplot(121)
fig.subplots_adjust(wspace=.55)
#plt.plot(time/Te,(KE_qg-KE_qg[0])/KE0,label=r"$K_e$",linewidth=lw,alpha=alp)
#plt.plot(time/Te,(PE_niw-PE_niw[0])/KE0,label=r'$P_w$',linewidth=lw,alpha=alp)
plt.plot(time/Te,(KE_niw-KE_niw[0])/KE_niw[0],label=r"$\Delta\langle\mathcal{A}\rangle/\langle\mathcal{A}\rangle(0)$",linewidth=lw,alpha=alp)
plt.plot(time/Te,(KE_qg-KE_qg[0])/KE0,label=r"$\Delta\langle\mathcal{K}\rangle/\langle\mathcal{K}\rangle(0)$",linewidth=lw,alpha=alp)
plt.plot(time/Te,(PE_niw-PE_niw[0])/KE0,label=r'$\Delta\langle\mathcal{P}\rangle/\langle\mathcal{K}\rangle(0)$',linewidth=lw,alpha=alp)

plt.plot(time/Te,(PE_niw-PE_niw[0]+KE_qg-KE_qg[0])/KE0,'--',
        label=r'$(\Delta\langle\mathcal{P}\rangle+\Delta\langle\mathcal{K}\rangle)/\langle\mathcal{K}\rangle(0)$',
        linewidth=lw,alpha=alp)
plt.ylim(-0.75,0.75)
plt.ylabel(r'Energy change about $t=0$')
plt.legend(loc=(0.05,1.))
plt.plot([0,tmax/Te],[0]*2,'-',linewidth=1,color="0.5")
plot_fig_label(ax, label="a",xc=0.05,yc = 0.05)
plt.xlabel(r"Time [$t \times U_e k_e$]")
plt.xticks([0,10,20,30,40,50])
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax = fig.add_subplot(122)
fig.subplots_adjust(wspace=.45)
plt.plot(time/Te,Te*g1/KE0,label=r'$\Gamma_r$',linewidth=lw,alpha=alp)
plt.plot(time/Te,Te*g2/KE0,label=r'$\Gamma_a$',linewidth=lw,alpha=alp)
plt.plot(time/Te,Te*chi_phi/KE0,label=r'$\varepsilon_\mathcal{P}$',linewidth=lw,alpha=alp)
plt.plot(time/Te,Te*(g1+g2+chi_phi)/KE0,label=r'$\Gamma_r+\Gamma_a+ \varepsilon_\mathcal{P}$',
                        linewidth=lw,alpha=alp)

plt.plot(time/Te,Te*dPE/KE0,'k--',label=r'$\mathrm{d}\langle\mathcal{P}\rangle/\mathrm{d}t$',linewidth=lw,alpha=alp)

#plt.legend(loc=1,ncol=1)
plt.legend(loc=(0.55,.9))
plt.xlabel(r"Time [$t \times U_e k_e$]")
plt.ylim(-0.35,0.35)
plt.ylabel(r'Power $[\dot P_w \times {2 k_e}/{U_e}^2 ]$')
plot_fig_label(ax, label="b",xc=0.05,yc = 0.05)
plt.xticks([0,10,20,30,40,50])

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

#fig = plt.figure(figsize=(8.5,6.))
#lw, alp = 3.,.5
#KE0 = KE_qg[0]
#tmax = time[-1]
#
#ax = fig.add_subplot(221)
#plt.plot(time/Te,(KE_qg-KE_qg[0])/KE0,label=r"$K_e$",linewidth=lw,alpha=alp)
#plt.plot(time/Te,(PE_niw-PE_niw[0])/KE0,label=r'$P_w$',linewidth=lw,alpha=alp)
#plt.xticks([])
#plt.ylim(-0.32,0.32)
#plt.ylabel(r'Energy  change $[(E-E_0) \times {2}/{U_e^2} ]$')
#plt.legend(loc=3)
#plt.plot([0,tmax/Te],[0]*2,'--',color="0.5")
#fig.subplots_adjust(wspace=.4)
#plot_fig_label(ax, label="a")
#
#ax = fig.add_subplot(222)
#plt.plot(time/Te,Te*g1/KE0,label=r'$\Gamma_r$',linewidth=lw,alpha=alp)
#plt.plot(time/Te,Te*g2/KE0,label=r'$\Gamma_a$',linewidth=lw,alpha=alp)
#plt.plot(time/Te,Te*chi_phi/KE0,label=r'$\chi_\phi$',linewidth=lw,alpha=alp)
#plt.plot(time/Te,Te*(g1+g2+chi_phi)/KE0,label=r'$\Gamma_r+\Gamma_a+\chi_\phi$',
#                        linewidth=lw,alpha=alp)
#plt.plot(time/Te,Te*dPE/KE0,'k--',label=r'$\dot P_w$',linewidth=lw,alpha=alp)
#plt.legend(loc=1,ncol=2)
#plt.xticks([])
#plt.ylim(-0.005,0.0125)
#plt.ylabel(r'Power $[\dot E \times {2 k_e}/{U_e} ]$')
#plot_fig_label(ax, label="b")
#
#ax = fig.add_subplot(223)
#plt.plot(time/Te,Te*pi/KE0,label=r'$\Pi$',linewidth=lw,alpha=alp)
#plt.plot(time/Te,Te*ep_psi/KE0,label=r'$\epsilon_\phi$',linewidth=lw,alpha=alp)
#plt.plot(time/Te,Te*(pi+ep_phi)/KE0,label=r'$\Pi+\epsilon_\phi$',linewidth=lw,alpha=alp)
#plt.plot(time/Te,Te*diKE_niw/KE0,'k--',label=r'$\dot K_w^i$'
#                ,linewidth=lw,alpha=alp)
#plt.xlabel(r"Time [$t \times U_e k_e$]")
#plt.ylabel(r'Power $[\dot E \times {2 k_e}/{U_e} ]$')
#plt.legend(loc=1,ncol=2)
#plot_fig_label(ax, label="c")
#
#fig.subplots_adjust(hspace=.125)
#
#ax = fig.add_subplot(224)
#p1 = ax.plot(time/Te,conc_niw,linewidth=lw,alpha=alp,label='NIW concentration, $C$')
#plt.ylabel(r"Wave-vorticity correlation [r]")
#plt.xlabel(r"Time [$t \times U_e k_e$]")
#plt.plot([0,tmax/Te],[0]*2,'--',color="0.5")
#plt.ylim(-0.8,0.4)
#plot_fig_label(ax, label="d")
#
plt.savefig(patho+"figsinxsiny.pdf", bbox_inches='tight')
plt.savefig(patho+"fig14.tiff", bbox_inches='tight')
