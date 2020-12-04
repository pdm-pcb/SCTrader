from requests.structures import CaseInsensitiveDict

planetary_system = CaseInsensitiveDict({
    "Cellin":        "Crusader",
    "Daymar":        "Crusader",
    "Yela":          "Crusader",
    "Port Olisar":   "Crusader",
    "Grim Hex":      "Crusader",
    "Crusader":      "Crusader",
    "Delamar":       "Delamar",
    "Arial":         "Hurston",
    "Aberdeen":      "Hurston",
    "Magda":         "Hurston",
    "Ita":           "Hurston",
    "Everus Harbor": "Hurston",
    "Hurston":       "Hurston",
    "Lyria":         "ArcCorp",
    "Wala":          "ArcCorp",
    "Baijini Point": "ArcCorp",
    "ArcCorp":       "ArcCorp",
    "Port Tressler": "MicroTech",
    "MicroTech":     "MicroTech",
    "Calliope":      "MicroTech",
    "Euterpe":       "MicroTech",
    "Clio":          "MicroTech"
})

travel_distance = CaseInsensitiveDict({
    "Delamar": {
        "ArcCorp":   49800000,
        "Crusader":  22500000,
        "Hurston":   29700000,
        "MicroTech": 38000000,
        "Delamar":   1
    },
    "ArcCorp": {
        "Delamar":   49800000,
        "Crusader":  42300000,
        "Hurston":   22900000,
        "MicroTech": 59500000,
        "ArcCorp":   1
    },
    "Crusader": {
        "Delamar":   22500000,
        "ArcCorp":   42300000,
        "MicroTech": 57500000,
        "Hurston":   31900000,
        "Crusader":  1
    },
    "Hurston": {
        "Delamar":   29700000,
        "ArcCorp":   22900000,
        "Crusader":  31900000,
        "MicroTech": 38400000,
        "Hurston":   1
    },
    "MicroTech": {
        "Delamar":   29700000,
        "ArcCorp":   22900000,
        "Crusader":  31900000,
        "MicroTech": 1,
        "Hurston":   38400000
    }
})
