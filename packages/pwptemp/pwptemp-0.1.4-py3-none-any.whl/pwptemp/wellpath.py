from numpy import interp, arange
from math import radians, sin, cos


def get(mdt, deltaz=50, profile='V', build_angle=1, kop=0, eob=0, sod=0, eod=0, kop2=0, eob2=0):
    if profile == 'V':        # Vertical well
        md = list(arange(0, mdt + deltaz, deltaz))  # Measured Depth from RKB, m
        tvd = md   # True Vertical Depth from RKB, m
        zstep = len(md)  # Number of cells from RKB up to the bottom
        horizontal = [0] * zstep  # x axis

    if profile == 'J':        # J-type well
        # Vertical section
        md = list(arange(0, mdt + deltaz, deltaz))  # Measured Depth from RKB, m
        tvd = md[:round(kop / deltaz) + 1]  # True Vertical Depth from RKB, m
        horizontal = [0] * len(tvd)   # x axis

        # Build section
        s = deltaz
        theta_delta = radians(build_angle / round((eob - kop) / deltaz))
        theta = theta_delta
        r = s / theta

        z_vertical = tvd[-1]
        z_displacement = (r * sin(theta))
        tvd.append(round(tvd[-1] + z_displacement, 2))

        hz_displacement = r * (1 - cos(theta))
        horizontal.append(round(horizontal[-1] + hz_displacement, 2))

        for x in range(round((eob - kop) / deltaz)-1):
            theta += theta_delta

            z_displacement = (r * sin(theta))
            tvd.append(round(z_vertical + z_displacement, 2))

            hz_displacement = r * (1 - cos(theta)) - horizontal[-1]
            horizontal.append(round(horizontal[-1] + hz_displacement, 2))

        # Tangent section
        z_displacement = (deltaz * cos(radians(build_angle)))
        hz_displacement = (deltaz * sin(radians(build_angle)))
        for x in range(round((mdt-eob)/deltaz)):
            tvd.append(round(tvd[-1] + z_displacement, 2))
            horizontal.append(round(horizontal[-1] + hz_displacement, 2))

        zstep = len(md)  # Number of cells from RKB up to the bottom

    if profile == 'S':  # S-type well
        # Vertical section
        md = list(arange(0, mdt + deltaz, deltaz))  # Measured Depth from RKB, m
        tvd = md[:round(kop / deltaz) + 1]  # True Vertical Depth from RKB, m
        horizontal = [0] * len(tvd)  # x axis

        # Build section
        s = deltaz
        theta_delta = radians(build_angle) / round((eob - kop) / deltaz)
        theta = theta_delta
        r = s / theta

        z_displacement = (r * sin(theta))
        tvd.append(round(tvd[-1] + z_displacement, 2))
        z_count = z_displacement

        hz_displacement = r * (1 - cos(theta))
        horizontal.append(round(horizontal[-1] + hz_displacement, 2))

        for x in range(round((eob - kop) / deltaz) - 1):
            theta = theta + theta_delta
            z_displacement = (r * sin(theta)) - z_count
            tvd.append(round(tvd[-1] + z_displacement, 2))
            z_count += z_displacement

            hz_displacement = r * (1 - cos(theta)) - horizontal[-1]
            horizontal.append(round(horizontal[-1] + hz_displacement, 2))

        # Tangent section
        z_displacement = (deltaz * cos(radians(build_angle)))
        hz_displacement = (deltaz * sin(radians(build_angle)))

        for x in range(round((sod - eob) / deltaz)):
            tvd.append(round(tvd[-1] + z_displacement, 2))
            horizontal.append(round(horizontal[-1] + hz_displacement, 2))

        # Drop section
        s = deltaz
        cells_drop = round((eod - sod) / deltaz)
        theta_delta = radians(build_angle) / cells_drop
        theta = radians(build_angle)
        r = s / theta_delta
        z_checkpoint = tvd[-1]
        hz_checkpoint = horizontal[-1]

        for x in range(cells_drop):
            z_displacement = r * (sin(theta) - sin(theta - (theta_delta * (x + 1))))
            tvd.append(round(z_checkpoint + z_displacement, 2))

            hz_displacement = r * (1 - cos(theta)) - r * (1 - cos(theta - (theta_delta * (x + 1))))
            horizontal.append(round(hz_checkpoint + hz_displacement, 2))

        # Vertical section
        for x in range(round((mdt - eod) / deltaz)):
            tvd.append(round(tvd[-1] + deltaz, 2))
            horizontal.append(horizontal[-1])  # x axis

        zstep = len(md)  # Number of cells from RKB up to the bottom

    if profile == 'H1':        # Horizontal single-curve well
        # Vertical section
        md = list(arange(0, mdt + deltaz, deltaz))  # Measured Depth from RKB, m
        tvd = md[:round(kop / deltaz) + 1]  # True Vertical Depth from RKB, m
        horizontal = [0] * len(tvd)  # x axis

        # Build section
        s = deltaz
        theta_delta = radians(90) / round((eob - kop) / deltaz)
        theta = theta_delta
        r = s / theta

        z_displacement = (r * sin(theta))
        tvd.append(round(tvd[-1] + z_displacement, 2))
        z_count = z_displacement

        hz_displacement = r * (1 - cos(theta))
        horizontal.append(round(horizontal[-1] + hz_displacement, 2))

        for x in range(round((eob - kop) / deltaz)-1):
            theta = theta+theta_delta
            z_displacement = (r * sin(theta)) - z_count
            tvd.append(round(tvd[-1] + z_displacement, 2))
            z_count += z_displacement

            hz_displacement = r * (1 - cos(theta)) - horizontal[-1]
            horizontal.append(round(horizontal[-1] + hz_displacement, 2))

        # Horizontal section
        for x in range(round((mdt-eob)/deltaz)):
            tvd.append(tvd[-1])
            horizontal.append(horizontal[-1] + deltaz)

        zstep = len(md)  # Number of cells from RKB up to the bottom

    if profile == 'H2':        # Horizontal double-curve well
        # Vertical section
        md = list(arange(0, mdt + deltaz, deltaz))  # Measured Depth from RKB, m
        tvd = md[:round(kop / deltaz) + 1]  # True Vertical Depth from RKB, m
        horizontal = [0] * len(tvd)  # x axis

        # Build section
        s = deltaz
        theta_delta = radians(build_angle / round((eob - kop) / deltaz))
        theta = theta_delta
        r = s / theta

        z_displacement = (r * sin(theta))
        tvd.append(round(tvd[-1] + z_displacement, 2))
        z_count = z_displacement

        hz_displacement = r * (1 - cos(theta))
        horizontal.append(round(horizontal[-1] + hz_displacement, 2))

        for x in range(round((eob - kop) / deltaz)-1):
            theta = theta + theta_delta
            z_displacement = (r * sin(theta)) - z_count
            tvd.append(round(tvd[-1] + z_displacement, 2))
            z_count += z_displacement

            hz_displacement = r * (1 - cos(theta)) - horizontal[-1]
            horizontal.append(round(horizontal[-1] + hz_displacement, 2))

        # Tangent section
        z_displacement = (deltaz * cos(radians(build_angle)))
        hz_displacement = (deltaz * sin(radians(build_angle)))
        for x in range(round((kop2-eob)/deltaz)):
            tvd.append(round(tvd[-1] + z_displacement, 2))
            horizontal.append(round(horizontal[-1] + hz_displacement, 2))

        # Build section 2
        s = deltaz
        build_angle = 90 - build_angle
        cells_drop = round((eob2 - kop2) / deltaz)
        theta_delta = radians(build_angle) / cells_drop
        theta = radians(build_angle)
        r = s / theta_delta
        z_checkpoint = tvd[-1]
        hz_checkpoint = horizontal[-1]

        for x in range(cells_drop):
            hz_displacement = r * (sin(theta) - sin(theta - (theta_delta * (x + 1))))
            horizontal.append(round(hz_checkpoint + hz_displacement, 2))

            z_displacement = r * (1 - cos(theta)) - r * (1 - cos(theta - (theta_delta * (x + 1))))
            tvd.append(round(z_checkpoint + z_displacement, 2))

        # Horizontal section
        for x in range(round((mdt - eob2) / deltaz)):
            tvd.append(tvd[-1])
            horizontal.append(horizontal[-1] + deltaz)

        zstep = len(md)  # Number of cells from RKB up to the bottom

    class WellDepths(object):
        def __init__(self):
            self.md = md
            self.tvd = tvd
            self.deltaz = deltaz
            self.zstep = zstep
            self.hd = horizontal

        def plot(self):
            import matplotlib.pyplot as plt
            # Plotting well profile (TVD vs Horizontal Displacement)
            plt.plot(self.hd, self.tvd, 'b')
            plt.xlabel('Horizontal Displacement, m')
            plt.ylabel('TVD, m')
            title = 'Well Profile'
            plt.title(title)
            plt.ylim(plt.ylim()[::-1])  # reversing y axis
            plt.show()

    return WellDepths()


def load(data, deltaz=50):

    if len(data) == 2:
        md = data[0]
        tvd = data[1]
    else:
        md = [x['md'] for x in data]
        tvd = [x['tvd'] for x in data]

    md_new = list(arange(0, max(md) + deltaz, deltaz))
    tvd_new = [0]
    for i in md_new[1:]:
        tvd_new.append(interp(i, md, tvd))
    zstep = len(md_new)

    class WellDepths(object):
        def __init__(self):
            self.md = md_new
            self.tvd = tvd_new
            self.deltaz = deltaz
            self.zstep = zstep

    return WellDepths()
