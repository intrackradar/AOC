
cali = {
    "name":"cali",
    "loopgain": 280,
    "location": {"lat":39, "lon":-121, "heightM":100},
    "fence":{"az":[270, 90],"el":[3.0]},
    "beamwidth":2.0,
    "frequency":450e6,
    "snrlimit": 4.0,
    "bandwidth": 10e6,
    "bandwidthPoints": 1,
    "losses": 0.0,
    "TXGain": 40,
    "RXGain": 40,
    "Power": 2.5e6,
    "PulseTime": 0.1
}

hawaii = {
    "name":"hawaii",
    "loopgain": 280,
    "location": {"lat":22, "lon":-159.76, "heightM":100},
    "fence":{"az":[270, 90],"el":[3.0]},
    "beamwidth":2.0,
    "frequency":450e6,
    "snrlimit": 4.0,
    "bandwidth": 10e6,
    "bandwidthPoints": 1,
    "losses": 0.0,
    "TXGain": 40,
    "RXGain": 40,
    "Power": 2.5e6,
    "PulseTime": 0.1
}

cape_cod = {
    "name":"cape cod",
    "loopgain": 310,
    "location": {"lat":42, "lon":-70, "heightM":10},
    "fence":{"az":[0, 360],"el":[3.0]},
    "beamwidth":2.0,
    "frequency":450e6,
    "snrlimit": 4.0,
    "bandwidth": 10e6,
    "bandwidthPoints": 1,
    "losses": 0.0,
    "TXGain": 39,
    "RXGain": 39,
    "Power": 2.5e6,
    "PulseTime": 0.1
}

thule = {
    "name":"thule",
    "loopgain": 310,
    "location": {"lat":76.5, "lon":-66.1, "heightM":10},
    "fence":{"az":[0, 360],"el":[3.0]},
    "beamwidth":2.0,
    "frequency": 450e6,
    "snrlimit": 4.0,
    "bandwidth": 10e6,
    "bandwidthPoints": 1,
    "losses": 0.0,
    "TXGain": 40,
    "RXGain": 40,
    "Power": 2.5e6,
    "PulseTime": 0.1
}

fylingdale450 = {
    "name":"fylingdale450",
    "loopgain": 310,
    "location": {"lat":57.6, "lon":-4.5, "heightM":10},
    "fence":{"az":[0, 360],"el":[3.0]},
    "beamwidth":2.0,
    "frequency": 450e6,
    "snrlimit": 4.0,
    "bandwidth": 10e6,
    "bandwidthPoints": 1,
    "losses": 0.0,
    "TXGain": 40,
    "RXGain": 40,
    "Power": 2.5e6,
    "PulseTime": 0.1
}

fylingdale300 = {
    "name":"fylingdale300",
    "loopgain": 310,
    "location": {"lat":57.6, "lon":-4.5, "heightM":10},
    "fence":{"az":[0, 360],"el":[3.0]},
    "beamwidth":2.0,
    "frequency": 300e6,
    "snrlimit": 4.0,
    "bandwidth": 10e6,
    "bandwidthPoints": 1,
    "losses": 0.0,
    "TXGain": 40,
    "RXGain": 40,
    "Power": 2.5e6,
    "PulseTime": 0.1
}
fylingdale600 = {
    "name":"fylingdale600",
    "loopgain": 310,
    "location": {"lat":57.6, "lon":-4.5, "heightM":10},
    "fence":{"az":[0, 360],"el":[3.0]},
    "beamwidth":2.0,
    "frequency": 600e6,
    "snrlimit": 4.0,
    "bandwidth": 10e6,
    "bandwidthPoints": 1,
    "losses": 0.0,
    "TXGain": 40,
    "RXGain": 40,
    "Power": 2.5e6,
    "PulseTime": 0.1

}

almond = {
    "name":"almond",
    "RCSData": {"450":{"url":"C:\\Users\\Jerem\\Downloads\\almond.xlsx","sheetname":"119in_450MHz_2degel","frequency":450e6},
                "300":{"url":"C:\\Users\\Jerem\\Downloads\\almond.xlsx","sheetname":"119in_300MHz","frequency":300e6},
                "600":{"url":"C:\\Users\\Jerem\\Downloads\\almond.xlsx","sheetname":"119in_600MHz","frequency":600e6}},
    "RocketStages":{"stage 1": {"fuel mass":30000, "isp": 300, "thrust": 790e3},
                    "stage 2": {"fuel mass":5000, "isp": 300, "thrust": 267e3},
                    "stage 3": {"fuel mass":3000, "isp": 300, "thrust": 155e3}
                    },
    "Launch Location":{"lat":35,"lon":51,"heightM":0},
    "Launch Time":"2025-01-01T01:01:00.000Z",
    "Headings":{"Heading 1":{"Time Range":["2025-01-01T01:01:00.000Z", "2025-01-01T01:01:30.000Z"],"Pointing":[0, 90]},
                "Heading 2":{"Time Range":["2025-01-01T01:01:30.000Z", "2025-01-01T01:06:30.000Z"],"Pointing":[317, 14]}
                },
    "Trajectory":"middleeasttrajectory.csv",
    "Aerodynamics":{"Cd":0.044,"A":2.2},
    "Drymass": 2000,
    "Propagator Time Step": 0.25,
    "azOffset": 0
}

almondhalf = {
    "name":"almondhalf",
    "RCSData": {"450half":{"url":"C:\\Users\\Jerem\\Downloads\\almond.xlsx","sheetname":"119in_450MHz_halfdeg","frequency":450e6},
                "300":{"url":"C:\\Users\\Jerem\\Downloads\\almond.xlsx","sheetname":"119in_300MHz","frequency":300e6},
                "600":{"url":"C:\\Users\\Jerem\\Downloads\\almond.xlsx","sheetname":"119in_600MHz","frequency":600e6}},
    "RocketStages":{"stage 1": {"fuel mass":30000, "isp": 300, "thrust": 790e3},
                    "stage 2": {"fuel mass":5000, "isp": 300, "thrust": 267e3},
                    "stage 3": {"fuel mass":3000, "isp": 300, "thrust": 155e3}
                    },
    "Launch Location":{"lat":35,"lon":51,"heightM":0},
    "Launch Time":"2025-01-01T01:01:00.000Z",
    "Headings":{"Heading 1":{"Time Range":["2025-01-01T01:01:00.000Z", "2025-01-01T01:01:30.000Z"],"Pointing":[0, 90]},
                "Heading 2":{"Time Range":["2025-01-01T01:01:30.000Z", "2025-01-01T01:06:30.000Z"],"Pointing":[317, 14]}
                },
    "Aerodynamics":{"Cd":0.044,"A":2.2},
    "Drymass": 2000,
    "Propagator Time Step": 0.25,
    "azOffset": 0
}
pencil = {
    "name":"pencil",
    "RCSData": {"450":{"url":"C:\\Users\\Jerem\\Downloads\\pencil.xlsx","sheetname":"18m_450MHz_halfdeg","frequency":450e6},
                "300":{"url":"C:\\Users\\Jerem\\Downloads\\pencil.xlsx","sheetname":"18m_300MHz","frequency":300e6},
                "600":{"url":"C:\\Users\\Jerem\\Downloads\\pencil.xlsx","sheetname":"18m_600MHz","frequency":600e6}},
    "RocketStages":{"stage 1": {"fuel mass":30000, "isp": 300, "thrust": 790e3},
                    "stage 2": {"fuel mass":5000, "isp": 300, "thrust": 267e3},
                    "stage 3": {"fuel mass":3000, "isp": 300, "thrust": 155e3}
                    },
    "Launch Location":{"lat":35,"lon":51,"heightM":0},
    "Launch Time":"2025-01-01T01:01:00.000Z",
    "Headings":{"Heading 1":{"Time Range":["2025-01-01T01:01:00.000Z", "2025-01-01T01:01:30.000Z"],"Pointing":[0, 90]},
                "Heading 2":{"Time Range":["2025-01-01T01:01:30.000Z", "2025-01-01T01:06:30.000Z"],"Pointing":[317, 14]}
                },
    "Aerodynamics":{"Cd":0.044,"A":2.2},
    "Drymass": 2000,
    "Propagator Time Step": 0.25,
    "azOffset": 180
}

pencil1m = {
    "name":"pencil_1m",
    "RCSData": {"450":{"url":"C:\\Users\\Jerem\\Downloads\\pencil.xlsx","sheetname":"1m_450MHz_quarterdeg","frequency":450e6},
                "300":{"url":"C:\\Users\\Jerem\\Downloads\\pencil.xlsx","sheetname":"1m_300MHz_quarterdeg","frequency":300e6},
                "600":{"url":"C:\\Users\\Jerem\\Downloads\\pencil.xlsx","sheetname":"1m_600MHz","frequency":600e6}},
    "RocketStages":{"stage 1": {"fuel mass":30000, "isp": 300, "thrust": 790e3},
                    "stage 2": {"fuel mass":5000, "isp": 300, "thrust": 267e3},
                    "stage 3": {"fuel mass":3000, "isp": 300, "thrust": 155e3}
                    },
    "Launch Location":{"lat":35,"lon":51,"heightM":0},
    "Launch Time":"2025-01-01T01:01:00.000Z",
    "Headings":{"Heading 1":{"Time Range":["2025-01-01T01:01:00.000Z", "2025-01-01T01:01:30.000Z"],"Pointing":[0, 90]},
                "Heading 2":{"Time Range":["2025-01-01T01:01:30.000Z", "2025-01-01T01:06:30.000Z"],"Pointing":[317, 14]}
                },
    "Aerodynamics":{"Cd":0.044,"A":2.2},
    # "Trajectory":"middleeasttrajectory.csv",
    "Drymass": 2000,
    "Propagator Time Step": 0.25,
    "azOffset": 180
}

pencil1mcache = {
    "name":"pencil_1m",
    "RCSData": {"450":{"url":"C:\\Users\\Jerem\\Downloads\\pencil.xlsx","sheetname":"1m_450MHz_quarterdeg","frequency":450e6},
                "300":{"url":"C:\\Users\\Jerem\\Downloads\\pencil.xlsx","sheetname":"1m_300MHz_quarterdeg","frequency":300e6},
                "600":{"url":"C:\\Users\\Jerem\\Downloads\\pencil.xlsx","sheetname":"1m_600MHz","frequency":600e6}},
    "RocketStages":{"stage 1": {"fuel mass":30000, "isp": 300, "thrust": 790e3},
                    "stage 2": {"fuel mass":5000, "isp": 300, "thrust": 267e3},
                    "stage 3": {"fuel mass":3000, "isp": 300, "thrust": 155e3}
                    },
    "Launch Location":{"lat":35,"lon":51,"heightM":0},
    "Launch Time":"2025-01-01T01:01:00.000Z",
    "Headings":{"Heading 1":{"Time Range":["2025-01-01T01:01:00.000Z", "2025-01-01T01:01:30.000Z"],"Pointing":[0, 90]},
                "Heading 2":{"Time Range":["2025-01-01T01:01:30.000Z", "2025-01-01T01:06:30.000Z"],"Pointing":[317, 14]}
                },
    "Aerodynamics":{"Cd":0.044,"A":2.2},
    "Trajectory":"middleeasttrajectory.csv",
    "Drymass": 2000,
    "Propagator Time Step": 0.25,
    "azOffset": 180
}
pencil1mhalf = {
    "name":"pencil_1m_half",
    "RCSData": {"450":{"url":"C:\\Users\\Jerem\\Downloads\\pencil.xlsx","sheetname":"1m_450MHZ_halfdeg","frequency":450e6},
                "300":{"url":"C:\\Users\\Jerem\\Downloads\\pencil.xlsx","sheetname":"1m_300MHz_halfdeg","frequency":300e6},
                "600":{"url":"C:\\Users\\Jerem\\Downloads\\pencil.xlsx","sheetname":"1m_600MHz","frequency":600e6}},
    "RocketStages":{"stage 1": {"fuel mass":30000, "isp": 300, "thrust": 790e3},
                    "stage 2": {"fuel mass":5000, "isp": 300, "thrust": 267e3},
                    "stage 3": {"fuel mass":3000, "isp": 300, "thrust": 155e3}
                    },
    "Launch Location":{"lat":35,"lon":51,"heightM":0},
    "Launch Time":"2025-01-01T01:01:00.000Z",
    "Headings":{"Heading 1":{"Time Range":["2025-01-01T01:01:00.000Z", "2025-01-01T01:01:30.000Z"],"Pointing":[0, 90]},
                "Heading 2":{"Time Range":["2025-01-01T01:01:30.000Z", "2025-01-01T01:06:30.000Z"],"Pointing":[317, 14]}
                },
    "Aerodynamics":{"Cd":0.044,"A":2.2},
    "Trajectory":"middleeasttrajectory.csv",
    "Drymass": 2000,
    "Propagator Time Step": 0.25,
    "azOffset": 180
}
sphere = {
    "name":"sphere",
    "RCSData": {"450":{"url":"C:\\Users\\Jerem\\Downloads\\sphere.xlsx","sheetname":"709in_450MHz","frequency":450e6},
                "300":{"url":"C:\\Users\\Jerem\\Downloads\\sphere.xlsx","sheetname":"709in_300MHz","frequency":300e6},
                "600":{"url":"C:\\Users\\Jerem\\Downloads\\sphere.xlsx","sheetname":"709in_600MHz","frequency":600e6}},
    "RocketStages":{"stage 1": {"fuel mass":30000, "isp": 300, "thrust": 790e3},
                    "stage 2": {"fuel mass":5000, "isp": 300, "thrust": 267e3},
                    "stage 3": {"fuel mass":3000, "isp": 300, "thrust": 155e3}
                    },
    "Launch Location":{"lat":35,"lon":51,"heightM":0},
    "Launch Time":"2025-01-01T01:01:00.000Z",
    "Headings":{"Heading 1":{"Time Range":["2025-01-01T01:01:00.000Z", "2025-01-01T01:01:30.000Z"],"Pointing":[0, 90]},
                "Heading 2":{"Time Range":["2025-01-01T01:01:30.000Z", "2025-01-01T01:06:30.000Z"],"Pointing":[317, 14]}
                },
    "Aerodynamics":{"Cd":0.044,"A":2.2},
    "Drymass": 2000,
    "Propagator Time Step": 0.25,
    "azOffset": 180
}

# pencil = {
#     "name":"pencil",
#     "RCSData": {"449.5":{"url":"C:\\Users\\Jerem\\Downloads\\pencil_rcs_4495_4505_460_300_450_600.xlsx","sheetname":"449_5","frequency":449.5e6},
#                 "450.5":{"url":"C:\\Users\\Jerem\\Downloads\\pencil_rcs_4495_4505_460_300_450_600.xlsx","sheetname":"450_5","frequency":450.5e6},
#                 "460":{"url":"C:\\Users\\Jerem\\Downloads\\pencil_rcs_4495_4505_460_300_450_600.xlsx","sheetname":"460","frequency":460e6},
#                 "300":{"url":"C:\\Users\\Jerem\\Downloads\\pencil_rcs_4495_4505_460_300_450_600.xlsx","sheetname":"300","frequency":300e6},
#                 "450":{"url":"C:\\Users\\Jerem\\Downloads\\pencil_rcs_4495_4505_460_300_450_600.xlsx","sheetname":"450","frequency":450e6},
#                 "600":{"url":"C:\\Users\\Jerem\\Downloads\\pencil_rcs_4495_4505_460_300_450_600.xlsx","sheetname":"600","frequency":600e6}},
#     "RocketStages":{"stage 1": {"fuel mass":30000, "isp": 300, "thrust": 790e3},
#                     "stage 2": {"fuel mass":5000, "isp": 300, "thrust": 267e3},
#                     "stage 3": {"fuel mass":3000, "isp": 300, "thrust": 155e3}
#                     },
#     "Launch Location":{"lat":35,"lon":51,"heightM":0},
#     "Launch Time":"2025-01-01T01:01:00.000Z",
#     "Headings":{"Heading 1":{"Time Range":["2025-01-01T01:01:00.000Z", "2025-01-01T01:01:30.000Z"],"Pointing":[0, 90]},
#                 "Heading 2":{"Time Range":["2025-01-01T01:01:30.000Z", "2025-01-01T01:06:30.000Z"],"Pointing":[317, 14]}
#                 },
#     "Aerodynamics":{"Cd":0.044,"A":2.2},
#     "Drymass": 2000,
#     "Propagator Time Step": 0.25
# }

tcone = {
    "name":"tcone",
    "RCSData": {"450":{"url":"C:\\Users\\Jerem\\Downloads\\AOC_az_el_450MHz_tcone (1).xlsx","sheetname":"tcone","frequency":450e6}},
    "RocketStages":{"stage 1": {"fuel mass":30000, "isp": 300, "thrust": 790e3},
                    "stage 2": {"fuel mass":5000, "isp": 300, "thrust": 267e3},
                    "stage 3": {"fuel mass":3000, "isp": 300, "thrust": 155e3}
                    },
    "Launch Location":{"lat":35,"lon":51,"heightM":0},
    "Launch Time":"2025-01-01T01:01:00.000Z",
    "Headings":{"Heading 1":{"Time Range":["2025-01-01T01:01:00.000Z", "2025-01-01T01:01:30.000Z"],"Pointing":[0, 90]},
                "Heading 2":{"Time Range":["2025-01-01T01:01:30.000Z", "2025-01-01T01:06:30.000Z"],"Pointing":[317, 14]}
                },
    "Aerodynamics":{"Cd":0.044,"A":2.2},
    "Drymass": 2000,
    "Propagator Time Step": 0.25
}

tcone2 = {
    "name":"tcone2",
    "RCSData": {"450":{"url":"C:\\Users\\Jerem\\Downloads\\AOC_az_el_450MHz_tcone (1).xlsx","sheetname":"30_8_80","frequency":450e6}},
    "RocketStages":{"stage 1": {"fuel mass":30000, "isp": 300, "thrust": 790e3},
                    "stage 2": {"fuel mass":5000, "isp": 300, "thrust": 267e3},
                    "stage 3": {"fuel mass":3000, "isp": 300, "thrust": 155e3}
                    },
    "Launch Location":{"lat":35,"lon":51,"heightM":0},
    "Launch Time":"2025-01-01T01:01:00.000Z",
    "Headings":{"Heading 1":{"Time Range":["2025-01-01T01:01:00.000Z", "2025-01-01T01:01:30.000Z"],"Pointing":[0, 90]},
                "Heading 2":{"Time Range":["2025-01-01T01:01:30.000Z", "2025-01-01T01:06:30.000Z"],"Pointing":[317, 14]}
                },
    "Aerodynamics":{"Cd":0.044,"A":2.2},
    "Drymass": 2000,
    "Propagator Time Step": 0.25
}

x29 = {
    "name":"x29",
    "RCSData": {"450":{"url":"C:\\Users\\Jerem\\Downloads\\AOC_az_el_450MHz_x29.xlsx","sheetname":"x29","frequency":450e6}},
    "RocketStages":{"stage 1": {"fuel mass":30000, "isp": 300, "thrust": 790e3},
                    "stage 2": {"fuel mass":5000, "isp": 300, "thrust": 267e3},
                    "stage 3": {"fuel mass":3000, "isp": 300, "thrust": 155e3}
                    },
    "Launch Location":{"lat":35,"lon":51,"heightM":0},
    "Launch Time":"2025-01-01T01:01:00.000Z",
    "Headings":{"Heading 1":{"Time Range":["2025-01-01T01:01:00.000Z", "2025-01-01T01:01:30.000Z"],"Pointing":[0, 90]},
                "Heading 2":{"Time Range":["2025-01-01T01:01:30.000Z", "2025-01-01T01:06:30.000Z"],"Pointing":[317, 14]}
                },
    "Aerodynamics":{"Cd":0.044,"A":2.2},
    "Drymass": 2000,
    "Propagator Time Step": 0.25
}

objects = {"x29":x29,"tcone":tcone,"tcone2":tcone2,"pencil":pencil,"pencil_1m_half":pencil1mhalf,"pencil_1m":pencil1m,"pencil_1m_cache":pencil1mcache,"almond":almond,"almondhalf":almondhalf,"sphere":sphere}
sensors = {"cali":cali, "hawaii": hawaii, "cape cod":cape_cod, "thule":thule,"fylingdale450":fylingdale450,"fylingdale300":fylingdale300,"fylingdale600":fylingdale600}
simulation = {"start time":"2025-01-01T01:01:00.000Z", "stop time":"2025-01-01T01:51:00.000Z","time step":1.0}