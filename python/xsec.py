def stop(mass = None):
    mass = int(mass)
    xs = {
        100: (559.757, 16.1085),
        105: (448.456, 15.9732),
        110: (361.917, 16.1134),
        115: (293.281, 15.9763),
        120: (240.077, 15.9212),
        125: (197.122, 15.7303),
        130: (163.376, 15.8101),
        135: (135.791, 15.8086),
        140: (113.319, 15.7234),
        145: (95.0292, 15.649),
        150: (80.268, 15.5946),
        155: (68.0456, 15.5232),
        160: (58.01, 15.3899),
        165: (49.6639, 15.3711),
        170: (42.6441, 15.3017),
        175: (36.7994, 15.1749),
        180: (31.8695, 15.2449),
        185: (27.7028, 15.063),
        190: (24.1585, 15.16),
        195: (21.1597, 14.9422),
        200: (18.5245, 14.9147),
        205: (16.2439, 15.117),
        210: (14.3201, 14.8495),
        215: (12.6497, 14.8689),
        220: (11.1808, 14.9108),
        225: (9.90959, 14.9662),
        230: (8.78125, 14.796),
        235: (7.81646, 14.7983),
        240: (6.96892, 14.7878),
        245: (6.22701, 14.7897),
        250: (5.57596, 14.7529),
        255: (5.00108, 14.729),
        260: (4.48773, 14.6782),
        265: (4.03416, 14.7964),
        270: (3.63085, 14.6565),
        275: (3.2781, 14.7341),
        280: (2.95613, 14.7816),
        285: (2.67442, 14.7661),
        290: (2.42299, 14.6805),
        295: (2.19684, 14.8465),
        300: (1.99608, 14.6905),
        305: (1.81486, 14.4434),
        310: (1.64956, 14.4769),
        315: (1.50385, 14.4549),
        320: (1.3733, 14.7503),
        325: (1.25277, 14.2875),
        330: (1.14277, 14.578),
        335: (1.04713, 14.3659),
        340: (0.959617, 14.3896),
        345: (0.879793, 14.3881),
        350: (0.807323, 14.3597),
        355: (0.74141, 14.368),
        360: (0.681346, 14.3357),
        365: (0.626913, 14.3627),
        370: (0.576882, 14.2712),
        375: (0.531443, 14.266),
        380: (0.489973, 14.3962),
        385: (0.452072, 14.2234),
        390: (0.4176, 14.3166),
        395: (0.385775, 14.3112),
        400: (0.35683, 14.2848),
        405: (0.329881, 14.2072),
        410: (0.305512, 14.2648),
        415: (0.283519, 14.102),
        420: (0.262683, 14.3075),
        425: (0.243755, 14.0504),
        430: (0.226367, 14.0494),
        435: (0.209966, 14.0334),
        440: (0.195812, 14.0772),
        445: (0.181783, 14.1771),
        450: (0.169668, 14.2368),
        455: (0.158567, 14.2609),
        460: (0.147492, 14.4105),
        465: (0.137392, 14.4772),
        470: (0.128326, 14.5144),
        475: (0.119275, 14.6664),
        480: (0.112241, 14.6307),
        485: (0.104155, 14.7581),
        490: (0.0977878, 14.7977),
        495: (0.091451, 14.8963),
        500: (0.0855847, 14.9611),
        505: (0.0801322, 15.0389),
        510: (0.0751004, 15.1402),
        515: (0.0703432, 15.2139),
        520: (0.0660189, 15.3368),
        525: (0.0618641, 15.4135),
        530: (0.0580348, 15.4422),
        535: (0.0545113, 15.5446),
        540: (0.0511747, 15.6283),
        545: (0.0481537, 15.726),
        550: (0.0452067, 15.8177),
        555: (0.0424781, 15.9022),
        560: (0.0399591, 16.0067),
        565: (0.0376398, 16.0367),
        570: (0.0354242, 16.137),
        575: (0.0333988, 16.2132),
        580: (0.0313654, 16.3135),
        585: (0.0295471, 16.4264),
        590: (0.0279395, 16.4546),
        595: (0.0263263, 16.567),
        600: (0.0248009, 16.6406),
        605: (0.0233806, 16.7295),
        610: (0.0220672, 16.8447),
        615: (0.0208461, 16.9276),
        620: (0.0196331, 17.0459),
        625: (0.0185257, 17.0835),
        630: (0.0175075, 17.1478),
        635: (0.0164955, 17.2753),
        640: (0.0155809, 17.3814),
        645: (0.0147721, 17.4885),
        650: (0.0139566, 17.56),
        655: (0.0132456, 17.6129),
        660: (0.0125393, 17.7363),
        665: (0.0118287, 17.7959),
        670: (0.0112223, 17.8974),
        675: (0.0106123, 17.9891),
        680: (0.0100516, 18.0618),
        685: (0.0095256, 18.1714),
        690: (0.0090306, 18.2108),
        695: (0.00856339, 18.3365),
        700: (0.0081141, 18.4146),
        705: (0.00769525, 18.4937),
        710: (0.00730084, 18.6195),
        715: (0.00692243, 18.7005),
        720: (0.00656729, 18.819),
        725: (0.00623244, 18.8796),
        730: (0.00591771, 18.996),
        735: (0.00561049, 19.0787),
        740: (0.00532605, 19.1995),
        745: (0.00506044, 19.2916),
        750: (0.00480639, 19.4088),
        755: (0.00455979, 19.508),
        760: (0.00433688, 19.632),
        765: (0.00412174, 19.7141),
        770: (0.00391839, 19.8299),
        775: (0.00372717, 19.9097),
        780: (0.00354211, 20.0016),
        785: (0.00336904, 20.123),
        790: (0.00320476, 20.2271),
        795: (0.00304935, 20.4479),
        800: (0.00289588, 20.516),
    }
    try:
        return xs[mass]
    except KeyError:
        var = 1
        while True:
            try:
                new = xs[mass+var]
                # print "Stop mass (%d) not in xsec dict. Using %s GeV." % (mass, mass+var)
                return new
            except KeyError:
                var += 1
            if var > 20:
                print mass
                print "Dodgy XS."
                return None