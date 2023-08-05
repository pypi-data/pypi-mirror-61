def data(casings=[], bit=0.216):
    from numpy import asarray
    dict = {'tin': 20.0, 'ts': 15.0, 'wd': 100.0,  'ddi': 4, 'ddo': 4.5, 'dri': 17.716, 'dro': 21, 'dfm': 80,
            'q': 47.696 * 16.667, 'lambdal': 0.635, 'lambdac': 43.3, 'lambdacem': 0.7, 'lambdad': 40.0, 'lambdafm': 2.249,
            'lambdar': 15.49, 'lambdaw': 0.6, 'cl': 3713.0, 'cc': 469.0, 'ccem': 2000.0, 'cd': 400.0, 'cr': 464.0,
            'cw': 4000.0, 'cfm': 800.0, 'h1': 1800.0, 'h2': 2000.0, 'h3': 200.0, 'h3r': 200.0, 'rhol': 1.198,
            'rhod': 7.6, 'rhoc': 7.8, 'rhor': 7.8, 'rhofm': 2.245, 'rhow': 1.029, 'rhocem': 2.7,
            'gt': 0.0238, 'wtg': -0.005, 'rpm': 100.0, 't': 2.0, 'tbit': 1.35, 'wob': 22.41, 'rop': 14.4, 'an': 3100.0}

    if len(casings) > 0:
        od = sorted([x['od'] * 0.0254 for x in casings])
        id = sorted([x['id'] * 0.0254 for x in casings])
        depth = sorted([x['depth'] for x in casings], reverse=True)
        dict['casings'] = [[od[x], id[x], depth[x]] for x in range(len(casings))]
        dict['casings'] = asarray(dict['casings'])
    else:
        dict['casings'] = [[(bit + dict['dro'] * 0.0254), bit, 0]]
        dict['casings'] = asarray(dict['casings'])

    return dict


def info(about='all'):
    print("Use the ID of a parameter to change the default value (e.g. tdict['tin']=30 to change the fluid inlet "
          "temperature from the default value to 30° Celsius)")
    print('Notice that the information is provided as follows:' + '\n' +
          'parameter ID: general description, units' + '\n')

    tubular_parameters = 'VALUES RELATED TO TUBULAR SIZES' + '\n' + \
                         'ddi: drill string inner diameter, in' + '\n' + \
                         'ddo: drill string outer diameter, in' + '\n' + \
                         'dri: riser inner diameter, in' + '\n' + \
                         'dro: riser outer diameter, in' + '\n'

    conditions_parameters = 'PARAMETERS RELATED TO SIMULATION CONDITIONS' + '\n' + \
                            'ts: surface temperature, °C' + '\n' + \
                            'wd: water depth, m' + '\n' + \
                            'dfm: undisturbed formation diameter, m' + '\n'

    heatcoeff_parameters = 'PARAMETERS RELATED TO HEAT COEFFICIENTS' + '\n' + \
                           'lambdal: fluid - thermal conductivity, W/(m*°C)' + '\n' + \
                           'lambdac: casing - thermal conductivity, W/(m*°C)' + '\n' + \
                           'lambdacem: cement - thermal conductivity, W/(m*°C)' + '\n' + \
                           'lambdad: drill pipe - thermal conductivity, W/(m*°C)' + '\n' + \
                           'lambdafm: formation - thermal conductivity, W/(m*°C)' + '\n' + \
                           'lambdar: riser - thermal conductivity, W/(m*°C)' + '\n' + \
                           'lambdaw: water - thermal conductivity, W/(m*°C)' + '\n' + \
                           'cl: fluid - specific heat capacity, J/(kg*°C)' + '\n' + \
                           'cc: casing - specific heat capacity, J/(kg*°C)' + '\n' + \
                           'ccem: cement - specific heat capacity, J/(kg*°C)' + '\n' + \
                           'cd: drill pipe - specific heat capacity, J/(kg*°C)' + '\n' + \
                           'cr: riser - specific heat capacity, J/(kg*°C)' + '\n' + \
                           'cw: water - specific heat capacity, J/(kg*°C)' + '\n' + \
                           'cfm: formation - specific heat capacity, J/(kg*°C)' + '\n' + \
                           'h1: drill pipe inner - convective heat transfer coefficient, W/(m^2*°C)' + '\n' + \
                           'h2: drill pipe outer - convective heat transfer coefficient, W/(m^2*°C)' + '\n' + \
                           'h3: casing inner - convective heat transfer coefficient, W/(m^2*°C)' + '\n' + \
                           'h3r: riser inner - convective heat transfer coefficient, W/(m^2*°C)' + '\n' + \
                           'gt: geothermal gradient, °C/m' + '\n' + \
                           'wtg: seawater thermal gradient, °C/m' + '\n'

    densities_parameters = 'PARAMETERS RELATED TO DENSITIES' + '\n' + \
                           'rhol: fluid density, sg' + '\n' + \
                           'rhod: drill pipe density, sg' + '\n' + \
                           'rhoc: casing density, sg' + '\n' + \
                           'rhor: riser density, sg' + '\n' + \
                           'rhofm: formation density, sg' + '\n' + \
                           'rhow: seawater density, sg' + '\n' + \
                           'rhocem: cement density, sg' + '\n'

    operational_parameters = 'PARAMETERS RELATED TO THE OPERATION' + '\n' + \
                             'tin: fluid inlet temperature, °C' + '\n' + \
                             'q: flow rate, lpm' + '\n' + \
                             'rpm: revolutions per minute' + '\n' + \
                             't: torque on the drill string, kN*m' + '\n' + \
                             'tbit: torque on the bit, kN*m' + '\n' + \
                             'wob: weight on bit, kN' + '\n' + \
                             'rop: rate of penetration, m/h' + '\n' + \
                             'an: area of the nozzles, in2' + '\n'

    if about == 'casings':
        print(tubular_parameters)

    if about == 'conditions':
        print(conditions_parameters)

    if about == 'heatcoeff':
        print(heatcoeff_parameters)

    if about == 'densities':
        print(densities_parameters)

    if about == 'operational':
        print(operational_parameters)

    if about == 'all':
        print(tubular_parameters + '\n' + conditions_parameters + '\n' + heatcoeff_parameters + '\n' +
              densities_parameters + '\n' + operational_parameters)


def set_well(temp_dict, depths):
    from math import pi
    from .main import stab_time
    from .analysis import hs_effect

    class NewWell(object):
        def __init__(self):
            # DEPTH
            self.md = depths.md
            self.tvd = depths.tvd
            self.deltaz = depths.deltaz
            self.zstep = depths.zstep

            # TUBULAR
            self.casings = temp_dict["casings"]  # casings array
            self.riser = round(temp_dict["wd"] / self.deltaz)  # number of grid cells for the riser
            self.ddi = temp_dict["ddi"] * 0.0254  # Drill String Inner  Diameter, m
            self.ddo = temp_dict["ddo"] * 0.0254   # Drill String Outer Diameter, m
            self.dri = temp_dict["dri"] * 0.0254  # Riser diameter Inner Diameter, m
            self.dro = temp_dict["dro"] * 0.0254   # Riser diameter Outer Diameter, m

            # CONDITIONS
            self.ts = temp_dict["ts"]  # Surface Temperature (RKB), °C
            self.wd = temp_dict["wd"]  # Water Depth, m
            self.dsr = self.casings[0, 0]  # Surrounding Space Inner Diameter, m
            self.dsro = self.casings[-1, 0] + 0.03  # Surrounding Space Outer Diameter, m
            self.dfm = temp_dict["dfm"]  # Undisturbed Formation Diameter, m

            # RADIUS (CALCULATED)
            self.r1 = self.ddi / 2  # Drill String Inner  Radius, m
            self.r2 = self.ddo / 2  # Drill String Outer Radius, m
            self.r3 = self.casings[0, 1] / 2  # Casing Inner Radius, m
            self.r3r = self.dri / 2  # Riser Inner Radius, m
            self.r4r = self.dro / 2  # Riser Outer Radius, m
            self.r4 = self.casings[0, 0] / 2  # Surrounding Space Inner Radius m
            self.r5 = self.dsro / 2  # Surrounding Space Outer Radius, m
            self.rfm = self.dfm / 2  # Undisturbed Formation Radius, m

            # HEAT COEFFICIENTS
            self.lambdal = temp_dict["lambdal"]  # Fluid
            self.lambdac = temp_dict["lambdac"]  # Casing
            self.lambdacem = temp_dict["lambdacem"]  # Cement
            self.lambdad = temp_dict["lambdad"]  # Drill Pipe
            self.lambdafm = temp_dict["lambdafm"]       # Formation
            self.lambdar = temp_dict["lambdar"]     # Riser
            self.lambdaw = temp_dict["lambdaw"]     # Seawater
            self.cl = temp_dict["cl"]       # Fluid
            self.cc = temp_dict["cc"]    # Casing
            self.ccem = temp_dict["ccem"]     # Cement
            self.cd = temp_dict["cd"]     # Drill Pipe
            self.cr = temp_dict["cr"]     # Riser
            self.cw = temp_dict["cw"]      # Seawater
            self.cfm = temp_dict["cfm"]       # Formation
            self.h1 = temp_dict["h1"]       # Drill Pipe inner wall
            self.h2 = temp_dict["h2"]       # Drill Pipe outer wall
            self.h3 = temp_dict["h3"]       # Casing inner wall
            self.h3r = temp_dict["h3r"]    # Riser inner wall
            self.gt = temp_dict["gt"] * self.deltaz  # Geothermal gradient, °C/m
            self.wtg = temp_dict["wtg"] * self.deltaz  # Seawater thermal gradient, °C/m

            # DENSITIES kg/m3
            self.rhol = temp_dict["rhol"] * 1000  # Fluid
            self.rhod = temp_dict["rhod"] * 1000  # Drill Pipe
            self.rhoc = temp_dict["rhoc"] * 1000  # Casing
            self.rhor = temp_dict["rhor"] * 1000  # Riser
            self.rhocem = temp_dict["rhocem"] * 1000  # Cement Sheath
            self.rhofm = temp_dict["rhofm"] * 1000  # Formation
            self.rhow = temp_dict["rhow"] * 1000  # Seawater

            # OPERATIONAL
            self.tin = temp_dict["tin"]  # Inlet Fluid temperature, °C
            self.q = temp_dict["q"] * 0.06    # Flow rate, m^3/h
            self.va = (self.q / (pi * ((self.r3 ** 2) - (self.r2 ** 2)))) / 3600   # Fluid velocity through the annular
            self.vp = (self.q / (pi * (self.r1 ** 2))) / 3600    # Fluid velocity through the drill pipe
            self.rpm = temp_dict["rpm"]    # Revolutions per minute
            self.t = temp_dict["t"]     # Torque on the drill string, kN*m
            self.tbit = temp_dict["tbit"]       # Torque on the bit, kN*m
            self.wob = temp_dict["wob"]     # Weight on bit, kN
            self.rop = temp_dict["rop"]     # Rate of Penetration, m/h
            self.an = temp_dict["an"] / 1550       # Area of the nozzles, m^2

            # Raise Errors:

            if self.casings[-1, 0] > self.dsro:
                raise ValueError('Last casing outer diameter must be smaller than the surrounding space diameter.')

            if self.casings[0, 2] > self.md[-1]:
                raise ValueError('MD must be higher than the first casing depth.')

            if self.casings[0, 1] < self.ddo:
                raise ValueError('Drill Pipe outer diameter must be smaller than the first casing inner diameter.')

            if self.wd > 0 and self.dro > self.dsro:
                raise ValueError('Riser diameter must be smaller than the surrounding space diameter.')

            if self.dsro > self.dfm:
                raise ValueError('Surrounding space diameter must be smaller than the undisturbed formation diameter.')

        def effect(self):
            effect = hs_effect(self)
            return effect

        def stab(self):
            result = stab_time(self)
            return result

    return NewWell()
