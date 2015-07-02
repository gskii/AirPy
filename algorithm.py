import math
class Algorithm(object):

    def start(self, degX, aminX, arcsecX, degY, aminY, arcsecY,
                    degD, aminD, arcsecD, speed):
        latitude  = self.__gradMinSec2Rad(degX, aminX, arcsecX) # Широта
        longitude = self.__gradMinSec2Rad(degY, aminY, arcsecY) # Долгота
        direction = self.__gradMinSec2Rad(degD, aminD, arcsecD) # Направление
        newLatLon = self.__getAzimutPoint(latitude, longitude, direction, speed * 0.000278)
        latitude  = self.__rad2GradMinSecX(newLatLon[0])        # (deg, amin, arcsec)X
        longitude = self.__rad2GradMinSecX(newLatLon[1])        # (deg, amin, arcsec)Y
        return (latitude, longitude)                            # return matrix
        
        
    def __gradMinSec2Rad(self, deg, amin, arcsec):
        return (deg + amin/60.0 + arcsec/3600.0)/57.2957795130

    def __getAzimutPoint(self, lat, lon, direct, length):
        '''Насколько я понимаю, функция вычисляет координату в следующий момент времени'''
        x2 = length * math.cos(direct)
        y2 = length * math.sin(direct)
        # const = 1.852 * 60 * 57.2957795130
        const = 6366.70701948456    
        lat2 = x2 / const + lat
        lon2 = y2 /(const * math.cos((2*lat + x2/const)/2.0)) + lon
        return (lat2, lon2)

    def __rad2GradMinSecX(self, rad):
        x = rad * 57.2957795130
        if x > 0:                   # Северная широта
            latType = 0
            deg     = int(x)
            temp    = (x - deg) * 60.
            amin    = int(temp)
            arcsec  = int((temp - amin) * 60.)
        else:                       # Южная широта
            latType = 1
            deg     = - int(x)
            amin    = - int((x + deg) * 60.)
            arcsec  = int(((x - deg) * 60. - amin) * 60.)
        return (deg, amin, arcsec)

    def __rad2GradMinSecY(self, rad):
        y = rad * 57.2957795130
        if y > 0:                   # Восточная долгота
            lonType = 0
            deg     = int(y)
            temp    = (y - deg) * 60.
            amin    = int(temp)
            arcsec  = int((temp - amin) * 60.)
        else:                       # Западная долгота
            lonType = 1
            deg     = - int(y)
            amin    = - int((y + deg) * 60.)
            arcsec  = int(((y - deg) * 60. - amin) * 60.)
        return (deg, amin, arcsec)
