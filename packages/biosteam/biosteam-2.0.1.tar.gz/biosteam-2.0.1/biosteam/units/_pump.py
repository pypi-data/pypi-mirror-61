# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 15:53:14 2018

@author: yoelr
"""
import numpy as np
from fluids.pump import nema_sizes_hp
from .designtools.mechanical import calculate_NPSH, pump_efficiency, nearest_NEMA_motor_size
from .._unit import Unit
from ..utils import static_flow_and_phase
import biosteam as bst

ln = np.log
exp = np.exp

# %% Data

max_hp = nema_sizes_hp[-1]

# Material factors
F_Mdict = {'Cast iron':       1,
           'Ductile iron':    1.15,
           'Cast steel':      1.35,
           'Bronze':          1.9,
           'Stainless steel': 2,
           'Hastelloy C':     2.95,
           'Monel':           3.3,
           'Nickel':          3.5,
           'Titanium':        9.7}

# Gear factor 
F_Tgear = {'OpenDripProof':           1,
           'EnclosedFanCooled':       1.4,
           'ExplosionProofEnclosure': 1.8}

# Centrifugal factor
F_Tcentrifugal = {'VSC3600':   1,
                  'VSC1800':   1.5,
                  'HSC3600':   1.7,
                  'HSC1800':   2,
                  '2HSC3600':  2.7,
                  '2+HSC3600': 8.9}

# Pump types
Types = ('CentrifugalSingle', 'CentrifugalDouble', 'Gear')
    

# %% Classes

# TODO: Fix pump selection to include NPSH available and required.
@static_flow_and_phase
class Pump(Unit):
    """Create a pump that sets the pressure of the 0th output stream.

    Parameters
    ----------
        P=None : float, optional
            Pressure of output stream (Pa). If None, cost pump as increase of pressure to P_startup.
    
    ins
        [0] Input stream
        
    outs
        [1] Output stream
    
    Examples
    --------
    :doc:`notebooks/Pump Example`
    
    References
    ----------
    [0] Seider, Warren D., et al. (2017). "Cost Accounting and Capital Cost Estimation". In Product and Process Design Principles: Synthesis, Analysis, and Evaluation (pp. 450-455). New York: Wiley.
    
    """
    _units = {'Ideal power': 'hp',
              'Power': 'hp',
              'Head': 'ft',
              'NPSH': 'ft',
              'Flow rate': 'gpm'}
    _has_power_utility = True
    BM = 3.3
    
    # Pump type
    _Type = 'Default'
    
    # Material factor
    _F_Mstr = 'Cast iron'
    _F_M = 1
    
    # Gear factor 
    _F_Tstr = 'VSC3600'
    _F_T = 1
    
    #: Pressure for costing purposes (Pa).
    P_startup = 405300 
    
    #: [bool] Ignore minimum NPSH requirement if True.
    ignore_NPSH = True

    @property
    def Type(self):
        """Pump type"""
        return self._Type
    @Type.setter
    def Type(self, Type):
        if Type not in Types:
            Types_str = str(Types)[1:-1]
            raise ValueError('Type must be one of the following: ' + Types_str)
        self._Type = Type
    
    @property
    def material(self):
        """Pump material"""
        return self._material
    @material.setter    
    def material(self, material):
        try:
            self._F_M = F_Mdict[material]
        except KeyError:
            dummy = str(F_Mdict.keys())[11:-2]
            raise ValueError(f"material must be one of the following: {dummy}")
        self._F_Mstr = material  
        
    def __init__(self, ID='', ins=None, outs=(), P=101325):
        super().__init__(ID, ins, outs)
        self.P = 101325
    
    def _setup(self):
        s_in, = self.ins
        s_out, = self.outs
        s_out.P = self.P
    
    def _run(self):
        s_in, = self.ins
        s_out, = self.outs
        s_out.T = s_in.T
    
    def _design(self):
        Design = self.design_results
        si, = self.ins
        so, = self.outs
        Pi = si.P
        Po = so.P
        Qi = si.F_vol
        mass = si.F_mass
        nu = si.nu
        dP = Po - Pi
        if dP < 1: dP = self.P_startup - Pi
        Design['Ideal power'] = power_ideal = Qi*dP*3.725e-7 # hp
        Design['Flow rate'] = q = Qi*4.403 # gpm
        if power_ideal <= max_hp:
            Design['Efficiency'] = efficiency = pump_efficiency(q, power_ideal)
            Design['Actual power'] = power = power_ideal/efficiency
            Design['Pump power'] = nearest_NEMA_motor_size(power)
            Design['N'] = N = 1
            Design['Head'] = head = power/mass*897806 # ft
            # Note that:
            # head = power / (mass * gravity)
            # head [ft] = power[hp]/mass[kg/hr]/9.81[m/s^2] * conversion_factor
            # and 897806 = (conversion_factor/9.81)
        else:
            power_ideal /= 2
            q /= 2
            if power_ideal <= max_hp:
                Design['Efficiency'] = efficiency = pump_efficiency(q, power_ideal)
                Design['Actual power'] = power = power_ideal/efficiency
                Design['Pump power'] = nearest_NEMA_motor_size(power)
                Design['N'] = N = 2
                Design['Head'] = head = power/mass*897806 # ft
            else:
                raise NotImplementedError('more than 2 pump required, but not yet implemented')
        
        if self.ignore_NPSH:
            NPSH_satisfied = True
        else:
            Design['NPSH'] = NPSH = calculate_NPSH(Pi, si.P_vapor, si.rho)
            NPSH_satisfied = NPSH > 1.52
        
        # Get type
        Type = self.Type
        if Type == 'Default':
            if (0.00278 < q < 5000
                and 15.24 < head < 3200
                and nu < 0.00002
                and NPSH_satisfied):
                Type = 'Centrifugal'
            elif (q < 1500
                  and head < 914.4
                  and 0.00001 < nu < 0.252):
                Type = 'Gear'
            elif (head < 20000
                  and q < 500
                  and power < 200
                  and nu < 0.01):
                Type = 'MeteringPlunger'
            else:
                NPSH = calculate_NPSH(Pi, si.P_vapor, si.rho)
                raise NotImplementedError(f'no pump type available at current power ({power:.3g} hp), flow rate ({q:.3g} gpm), and head ({head:.3g} ft), kinematic viscosity ({nu:.3g} m2/s), and NPSH ({NPSH:.3g} ft)')
                
        Design['Type'] = Type
        self.power_utility(power/N/1.341) # Set power in kW
    
    def _cost(self):
        # Parameters
        Design = self.design_results
        Cost = self.purchase_costs
        Type = Design['Type']
        q = Design['Flow rate']
        h = Design['Head']
        p = Design['Pump power']
        F_M = self._F_M
        I = bst.CE/567
        lnp = ln(p)
        
        # TODO: Add cost equation for small pumps
        # Head and flow rate is too small, so make conservative estimate on cost
        if q < 50: q = 50
        if h < 50: h = 50
        
        # Cost pump
        if 'Centrifugal' in Type:
            # Find pump factor
            F_Tdict = F_Tcentrifugal
            F_T = 1 # Assumption
            if p < 75 and 50 <= q <= 900 and 50 <= h <= 400:
                F_T = F_Tdict['VSC3600']
            elif p < 200 and 50 <= q <= 3500 and 50 <= h <= 2000:
                F_T = F_Tdict['VSC1800']
            elif p < 150 and 100 <= q <= 1500 and 100 <= h <= 450:
                F_T = F_Tdict['HSC3600']
            elif p < 250 and 250 <= q <= 5000 and 50 <= h <= 500:
                F_T = F_Tdict['HSC1800']
            elif p < 250 and 50 <= q <= 1100 and 300 <= h <= 1100:
                F_T = F_Tdict['2HSC3600']
            elif p < 1450 and 100 <= q <= 1500 and 650 <= h <= 3200:
                F_T = F_Tdict['2+HSC3600']
            else:
                raise NotImplementedError(f'no centrifugal pump available at current power ({p:.3g} hp), flow rate ({q:.3g} gpm), and head ({h:.3g} ft)')
            S = q*h**0.5 # Size factor
            S_new = S if S > 400 else 400
            lnS = ln(S_new)
            Cb = exp(12.1656-1.1448*lnS+0.0862*lnS**2)
            Cb *= S/S_new
            Cost['Pump'] = F_M*F_T*Cb*I
        elif Type == 'Gear':
            q_new = q if q > 50 else 50
            lnq = ln(q_new)
            Cb = exp(8.2816 - 0.2918*lnq + 0.0743*lnq**2)
            Cb *= q/q_new
            Cost['Pump'] = F_M*Cb*I
        elif Type == 'MeteringPlunger':
            Cb = exp(7.9361 + 0.26986*lnp + 0.06718*lnp**2)
            Cost['Pump'] = F_M*Cb*I
        
        # Cost electric motor
        lnp2 = lnp**2
        lnp3 = lnp2*lnp
        lnp4 = lnp3*lnp
        Cost['Motor'] = exp(5.9332 + 0.16829*lnp
                            - 0.110056*lnp2 + 0.071413*lnp3
                            - 0.0063788*lnp4)*I
    
        
        
        