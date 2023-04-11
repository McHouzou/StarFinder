import numpy as np
import datetime as dtm
from datetime import timedelta
import sys
import time

def extract_equatorial(fname, target_name):
    """
    Extract Right Ascension & Declination given target (star, Messier Object etc.) name
    """

    filein = open(fname, "r")
    S = filein.readlines()
    filein.close()

    if fname == "Stars.txt":
        for i in range (len(S)):
            S[i] = S[i].split('   ')
            if S[i][0] == target_name:
                RA = (int(S[i][1][0]+S[i][1][1]) + int(S[i][1][4]+S[i][1][5])/60)*15
                d = float(S[i][2][:-2])
                break

    if fname == "Messier.txt":
        for i in range (len(S)):
            S[i] = S[i].split(' ')
            if S[i][0] == target_name:
                RA = (float(S[i][1][:-1]) + float(S[i][2][:-1])/60)*15
                sign = 1
                if S[i][3][0] == '\U00002013' or S[i][3][0] == '-':
                    sign = -1
                d = sign*(float(S[i][3][1:-1]) + float(S[i][4][:-1])/60)

    return RA, d


def GMST(plus_UT): #e.g. if timezone is UT+3, plus_UT = 3
    """
    Find GMST
    """

    dnow = dtm.datetime.now() - timedelta(hours=plus_UT)
    d0 = dtm.datetime(2000, 1, 1, 12, 0)

    D = dnow - d0
    D = (D.days + D.seconds/(24*3600))
    GMST = (18.697374558 + 24.06570982441908*D)%24
    t = dtm.time(int(GMST//1), int((GMST%1)*60), int((GMST%1*60 - int((GMST%1)*60))*60))
    #print(f"GMST: {t}")
    return GMST, t


def extract_coordinates(fname, city, country):
    """
    Extract longtitude & latitude given city name
    """

    trgt = [city, country]

    filein = open(fname, "r")
    C = filein.readlines()
    filein.close()

    for i in range (len(C)):
        C[i] = C[i].split('\t')
        if (C[i][0] == trgt[0]) and (C[i][3][:-1] == trgt[1]):
            lat = float(C[i][1])
            lng = float(C[i][2])
            break

    return lat, lng


def hour_angle(GMST, RA, lng):
    H = GMST*15 - RA + lng
    return H


def alt_az(plus_UT, fname_s, fname_c, target_name, city, country):

    """
    Find altitude & azimuth given all the above
    """

    lat,lng = extract_coordinates(fname_c, city, country)
    RA, d = extract_equatorial(fname_s, target_name)
    gmst, t = GMST(plus_UT)
    H = hour_angle(gmst, RA, lng)

    lat = lat*np.pi/180
    d = d*np.pi/180
    H = H*np.pi/180

    alt = np.arcsin(np.cos(lat)*np.cos(d)*np.cos(H) + np.sin(lat)*np.sin(d))
    As = -(np.sin(H)*np.cos(d))/np.cos(alt)
    Ac = (np.sin(d)-np.sin(lat)*np.sin(alt))/(np.cos(lat)*np.cos(alt))

    A = np.arctan2(As, Ac)

    if A<0:
        A = 2*np.pi + A

    #print(f"Altitude: {np.degrees(alt):.3f}°")
    #print(f"Azimuth: {np.degrees(A):.3f}°")
    return alt, A, t


def live_pos():
    print('\n' + f"Live position in alt-azimuthian coordinates of {target_name} as seen from {city}, {country}" + '\n')
    while True:
        alt, Az, t = alt_az(plus_UT, fname_s, fname_c, target_name, city, country)
        print (f" GMST: {t}    Altitude: {np.degrees(alt):.5f}°    Azimuth: {np.degrees(Az):.5f}°", end="", flush=True),
        print("\r", end="", flush=True)
        time.sleep(1)

plus_UT = 3
fname_s = "Stars.txt"
fname_c = "Cities.txt"
target_name = input("Please give target name: ")
city = "Ródos"
country = "Greece"

live_pos()
