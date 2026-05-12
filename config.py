# ─────────────────────────────────────────────────────────────────────────────
# config.py  —  All static data: airports, waypoints, routes, performance model
# Source: LROP.docx / RUTE.docx (coordinates verified against AIP)
# ─────────────────────────────────────────────────────────────────────────────

AIRPORTS = {
    "LROP": {"name": "Bucharest Henri Coandă",  "lat": 44.5717, "lon": 26.0850, "elev": 314},
    "LHBP": {"name": "Budapest Ferenc Liszt",    "lat": 47.4400, "lon": 19.2617, "elev": 495},
    "LIRF": {"name": "Rome Fiumicino",           "lat": 41.8000, "lon": 12.2383, "elev":  14},
    "LEBL": {"name": "Barcelona El Prat",        "lat": 41.2967, "lon":  2.0783, "elev":  12},
    "EHAM": {"name": "Amsterdam Schiphol",       "lat": 52.3083, "lon":  4.7650, "elev":  11},
    "EDDF": {"name": "Frankfurt Main",           "lat": 50.0333, "lon":  8.5700, "elev": 364},
    "EGLL": {"name": "London Heathrow",          "lat": 51.4783, "lon": -0.4617, "elev":  83},
    "LFPG": {"name": "Paris Charles de Gaulle", "lat": 49.0100, "lon":  2.5483, "elev": 392},
}

# Departure airports and their valid destinations (from LROP.docx)
DEPARTURES  = ["LROP", "LHBP", "LIRF", "LEBL"]
VALID_DEST  = {d: ["EHAM", "EDDF", "EGLL", "LFPG"] for d in DEPARTURES}

# Fixed aircraft and cruise level for all flights
ACTYPE      = "A321N"
CRUISE_FL   = 360
CRUISE_ALT_FT = 36_000

# ── Waypoints (AIP-verified coordinates from LROP.docx) ──────────────────────
WAYPOINTS = {
    "ABETI":(47.6783,17.0133), "ADABI":(46.5617, 0.5300), "ADITA":(43.2283, 5.8283),
    "ADKUV":(50.5067, 6.8183), "ADUTO":(50.5150, 3.3617), "AGN":  (43.8883, 0.8733),
    "AKINI":(48.7500,12.1250), "AMRAX":(48.0917,19.3667), "AMTEL":(43.2200,11.6083),
    "AOSTA":(45.7967, 7.3450), "ARSAF":(49.3500, 2.1350), "ASPAT":(49.1967,10.7250),
    "BAMES":(48.9750, 1.4867), "BEGLA":(47.8300,17.1150), "BETEX":(49.8150, 6.4250),
    "BODRU":(44.2083, 6.3783), "BOKNO":(47.0467, 0.6917), "BOLRO":(50.0000,-1.6917),
    "BOMBI":(50.0567, 8.8000), "BORMI":(46.0367,11.1667), "BUB":  (50.9017, 4.5383),
    "CMB":  (50.2283, 3.1517), "CNA":  (45.6600,-0.3117), "COSTA":(51.3483, 3.3550),
    "DALIN":(41.7333, 3.3583), "DEBHI":(49.3600,10.4667), "DEGET":(46.4933,21.2667),
    "DEMAB":(50.5417, 9.9550), "DENUT":(51.2367, 3.6583), "DEVRO":(47.4950, 0.7383),
    "DEXIT":(48.7633,13.7100), "DIBER":(42.0800, 4.4150), "DIRER":(44.9883,21.4100),
    "DITIS":(48.8983,15.1167), "EGOZE":(49.5533, 2.4900), "EKRAS":(48.9000,-1.5000),
    "ELMEK":(49.9033,14.0300), "EMPAX":(48.4617, 8.9983), "EPAPU":(47.7100,-1.4117),
    "EPL":  (48.3183, 6.0600), "ERNAS":(48.8450,11.2200), "ESOKO":(45.8783, 7.0967),
    "ETASA":(49.1900, 9.1283), "EVNAM":(43.6050, 1.1133), "FERDI":(50.9133, 3.6367),
    "GAPLA":(50.6533,10.2800), "GILEP":(47.4833,18.2583), "GILIR":(47.0633, 6.2400),
    "GILOM":(50.7517, 4.7733), "GIVRI":(47.2917, 5.3417), "GODRA":(46.5933, 7.7083),
    "GOLMO":(48.9633,11.0550), "GOLVA":(46.7067,15.6517), "GONBA":(48.6883,13.0750),
    "GOVGO":(43.1750,10.3350), "HAFUN":(48.6017, 9.7517), "HELEN":(51.2350, 3.8700),
    "IDOSA":(49.7417, 5.8700), "INBED":(49.3883,10.9417), "INLOD":(51.5800, 2.3583),
    "IRMAR":(44.8000, 6.7900), "IXILU":(47.7400, 6.0417), "JAZFI":(51.0950, 4.0350),
    "KATCE":(51.2517,10.3500), "KATQA":(49.0200,17.2417), "KEGIT":(51.4067, 3.1067),
    "KEPER":(47.8067, 0.2733), "KERAX":(50.4750, 9.5817), "KINES":(45.3317, 6.7550),
    "KOMOB":(50.1433, 5.3733), "LADOL":(48.1667, 8.9533), "LATBA":(50.4217,11.3217),
    "LBU":  (48.9133, 9.3400), "LENDO":(50.6250, 6.2783), "LOGAN":(51.7483, 1.6117),
    "LUSOL":(43.7717, 6.0783), "MAMOR":(48.8850,12.2217), "MANAK":(46.2133,-0.9417),
    "MAXIR":(43.3950, 6.0400), "MOGTI":(47.3883,10.7167), "MOLUS":(46.4433, 6.6800),
    "NATPI":(42.7233, 1.2350), "NAXAV":(46.4633,11.3217), "NEMAL":(47.9183,13.4983),
    "NEMBO":(42.2900,10.7767), "NIKWU":(47.9000,10.4167), "NIMDI":(48.8017,11.6333),
    "NIMER":(47.4733, 0.3567), "NORKU":(52.2150, 6.9767), "NURGO":(50.2650,12.0167),
    "OKABI":(42.6167, 1.4833), "OKTET":(44.4850, 6.5700), "OLASO":(48.2083,10.2317),
    "OLOXO":(42.4350, 1.5133), "ORSUD":(45.9583, 7.1817), "OTMUV":(44.1950, 9.0550),
    "OZE":  (46.4050,11.2917), "PENDU":(47.3483, 6.0333), "PEPAX":(47.0817, 0.4533),
    "PEROT":(45.4000,19.0133), "PIVUS":(41.9233, 3.9333), "PIWIZ":(48.2150, 1.0983),
    "POI":  (46.5817, 0.2983), "POLUN":(44.2367,25.2233), "RAPET":(50.1900,12.3383),
    "RAPOR":(49.5917, 5.2133), "RASIN":(46.0900,16.6750), "REDNI":(49.0800,10.8900),
    "REMBA":(50.6617, 4.9133), "RENKA":(48.5850,13.5050), "REVTU":(49.5967,-1.7250),
    "RINSO":(48.0267,-1.4350), "RITAX":(50.0783, 5.8067), "ROUSY":(49.4767, 6.1150),
    "ROXOG":(50.2667,-1.5617), "RUNEN":(50.5850,10.5850), "SASKI":(51.5483, 2.5000),
    "SECHE":(44.4383, 0.5150), "SIMBA":(48.2300,13.0150), "SOGRI":(50.8067, 5.0450),
    "SOKRU":(44.9933,25.3300), "SOLVU":(50.5017, 9.7400), "SOVAN":(42.8350,11.8917),
    "SPESA":(49.8617, 9.3483), "SPEZI":(43.7767, 9.5950), "STAUB":(48.7850,12.6583),
    "SUDUX":(46.9450,11.0083), "SUKON":(49.6600, 9.1950), "SUMUM":(51.6367, 2.1083),
    "SUPIX":(49.7283, 9.3050), "TEKNO":(47.6233,17.4083), "TINIL":(47.5883, 5.0983),
    "TOD":  (50.1117,-1.6383), "TOLVU":(49.6250, 5.3717), "TOU":  (43.6800, 1.3100),
    "UNIMI":(46.8600,11.0650), "UNKIR":(46.8150, 5.7267), "UVELI":(45.0417, 0.1117),
    "VADOM":(48.5500, 1.2700), "VAGAB":(50.5333,10.8167), "VANAD":(47.8367, 0.9067),
    "VANAS":(45.4567, 6.7467), "VARIK":(50.2917,12.3817), "VEDUS":(49.5950, 4.7817),
    "VEKIN":(50.4050, 3.2750), "VEXIL":(50.3917,12.6333), "VIBOM":(49.4667, 9.1550),
    "XINLA":(49.2833, 9.1417), "ZOLKU":(47.5567,17.8083),
}

# ── Routes (exact sequences from LROP.docx) ──────────────────────────────────
ROUTES = {
    "LROP-EHAM": (
        ["LROP","SOKRU","AMRAX","KATQA","ELMEK","VEXIL","KATCE","NORKU","EHAM"],
        ["DCT","DCT","DCT","DCT","DCT","DCT","DCT","DCT"]),
    "LROP-EDDF": (
        ["LROP","POLUN","DIRER","PEROT","RASIN","GOLVA","NEMAL","SIMBA","AKINI",
         "NIMDI","ERNAS","GOLMO","REDNI","ASPAT","DEBHI","EDDF"],
        ["DCT","DCT","DCT","DCT","DCT","DCT","DCT","T161","T161","T161","T161","T161","T161","T161","DCT"]),
    "LROP-EGLL": (
        ["LROP","SOKRU","DEGET","BEGLA","DEXIT","INBED","BOMBI","ADKUV","SOGRI",
         "DENUT","COSTA","KEGIT","SASKI","INLOD","SUMUM","LOGAN","EGLL"],
        ["DCT","DCT","DCT","DCT","DCT","DCT","DCT","DCT","L608","L608","L608","L608","L608","L608","L608","L608"]),
    "LROP-LFPG": (
        ["LROP","SOKRU","DEGET","ABETI","RENKA","GONBA","STAUB","MAMOR","ASPAT",
         "VIBOM","BETEX","IDOSA","TOLVU","RAPOR","VEDUS","LFPG"],
        ["DCT","DCT","DCT","L610","L610","L610","DCT","DCT","DCT","DCT","UN857","UN857","UZ157","UZ157","DCT"]),
    "LHBP-EHAM": (
        ["LHBP","GILEP","ZOLKU","BEGLA","DITIS","VARIK","KATCE","NORKU","EHAM"],
        ["DCT","DCT","DCT","DCT","DCT","DCT","DCT","DCT"]),
    "LHBP-EDDF": (
        ["LHBP","GILEP","ZOLKU","BEGLA","DITIS","RAPET","NURGO","LATBA","VAGAB",
         "RUNEN","GAPLA","DEMAB","SOLVU","KERAX","EDDF"],
        ["DCT","DCT","DCT","T170","T170","T178","T178","T178","T178","T178","T178","T178","DCT"]),
    "LHBP-EGLL": (
        ["LHBP","GILEP","ZOLKU","TEKNO","ABETI","RENKA","INBED","BOMBI","ADKUV",
         "LENDO","SOGRI","DENUT","COSTA","KEGIT","SASKI","INLOD","SUMUM","LOGAN","EGLL"],
        ["DCT","DCT","DCT","DCT","DCT","DCT","DCT","DCT","DCT","DCT","L608","L608","L608","L608","L608","L608","L608","L608"]),
    "LHBP-LFPG": (
        ["LHBP","GILEP","ZOLKU","TEKNO","ABETI","RENKA","ASPAT","VIBOM","BETEX",
         "IDOSA","TOLVU","RAPOR","VEDUS","LFPG"],
        ["DCT","DCT","DCT","DCT","DCT","DCT","DCT","DCT","DCT","DCT","DCT","DCT","DCT"]),
    "LIRF-EHAM": (
        ["LIRF","NEMBO","GOVGO","AOSTA","ORSUD","MOLUS","GILIR","PENDU","IXILU",
         "EPL","ROUSY","IDOSA","KOMOB","BUB","JAZFI","HELEN","EHAM"],
        ["DCT","DCT","DCT","DCT","DCT","DCT","DCT","DCT","DCT","DCT","DCT","Y28","Y28","Y28","Y28","DCT"]),
    "LIRF-EDDF": (
        ["LIRF","SOVAN","AMTEL","BORMI","OZE","NAXAV","UNIMI","SUDUX","MOGTI",
         "NIKWU","OLASO","HAFUN","LBU","ETASA","XINLA","SUKON","SUPIX","SPESA","EDDF"],
        ["DCT","DCT","DCT","DCT","DCT","L12","L12","Q163","Q163","Q163","Q163","Q163","T163","T163","T163","T163","T163","DCT"]),
    "LIRF-EGLL": (
        ["LIRF","NEMBO","GOVGO","SPEZI","OTMUV","AOSTA","ORSUD","MOLUS","GILIR",
         "PENDU","IXILU","EPL","ROUSY","RITAX","REMBA","GILOM","BUB","DENUT",
         "COSTA","KEGIT","SASKI","INLOD","SUMUM","LOGAN","EGLL"],
        ["DCT","DCT","DCT","DCT","DCT","DCT","DCT","DCT","DCT","DCT","DCT","M624","M624","M624","L608","L608","L608","L608","L608","L608","L608","L608","L608","L608"]),
    "LIRF-LFPG": (
        ["LIRF","NEMBO","GOVGO","AOSTA","ORSUD","MOLUS","UNKIR","GIVRI","TINIL","LFPG"],
        ["DCT","DCT","DCT","DCT","DCT","DCT","DCT","DCT","DCT"]),
    "LEBL-EHAM": (
        ["LEBL","OLOXO","OKABI","TOU","ADABI","BOKNO","DEVRO","VANAD","PIWIZ",
         "VADOM","BAMES","ARSAF","EGOZE","CMB","VEKIN","ADUTO","FERDI","DENUT","EHAM"],
        ["DCT","DCT","DCT","DCT","UN858","UN874","UN874","UN874","UN874","UN874","DCT","DCT","DCT","DCT","N873","N873","Y18","DCT"]),
    "LEBL-EDDF": (
        ["LEBL","DALIN","PIVUS","DIBER","ADITA","MAXIR","LUSOL","BODRU","OKTET",
         "IRMAR","KINES","VANAS","ESOKO","GODRA","LADOL","EMPAX","EDDF"],
        ["DCT","DCT","DCT","DCT","DCT","DCT","DCT","DCT","DCT","DCT","DCT","DCT","DCT","T163","T163","DCT"]),
    "LEBL-EGLL": (
        ["LEBL","NATPI","EVNAM","AGN","SECHE","UVELI","CNA","MANAK","EPAPU",
         "RINSO","EKRAS","REVTU","BOLRO","TOD","ROXOG","EGLL"],
        ["DCT","DCT","DCT","DCT","DCT","DCT","DCT","DCT","DCT","DCT","DCT","DCT","UP87","UP87","DCT"]),
    "LEBL-LFPG": (
        ["LEBL","OLOXO","OKABI","TOU","POI","PEPAX","NIMER","KEPER","LFPG"],
        ["DCT","DCT","DCT","DCT","UT182","UT182","UT182","DCT"]),
}

# ── A321N Performance Model (BADA-inspired) ───────────────────────────────────
PERF = {
    "climb_rate_fpm":  {0: 2800, 10000: 2200, 20000: 1700, 30000: 1100, 36000: 600},
    "desc_rate_fpm":   {36000: 1800, 20000: 2000, 10000: 1800, 3000: 1200},
    "climb_cas_lo_kt": 250,    # below 10,000 ft (ICAO speed restriction)
    "climb_cas_hi_kt": 300,    # 10,000 – ~28,000 ft
    "cruise_mach":     0.790,  # A321neo typical cruise Mach
    "desc_cas_kt":     300,
    "desc_mach":       0.785,
}
