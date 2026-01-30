
cali = {
    "name":"cali",
    "loopgain": 280,
    "location": {"lat":39, "lon":-121, "heightM":100},
    "fence":{"az":[270, 90],"el":[3.0]},
    "beamwidth":2.0,
    "frequency":450e6,
    "snrlimit": 4.0
}

hawaii = {
    "name":"hawaii",
    "loopgain": 280,
    "location": {"lat":22, "lon":-159.76, "heightM":100},
    "fence":{"az":[270, 90],"el":[3.0]},
    "beamwidth":2.0,
    "frequency":450e6,
    "snrlimit": 4.0
}

cape_cod = {
    "name":"cape cod",
    "loopgain": 310,
    "location": {"lat":42, "lon":-70, "heightM":10},
    "fence":{"az":[0, 360],"el":[3.0]},
    "beamwidth":2.0,
    "frequency":450e6,
    "snrlimit": 4.0
}

thule = {
    "name":"thule",
    "loopgain": 310,
    "location": {"lat":76.5, "lon":-66.1, "heightM":10},
    "fence":{"az":[0, 360],"el":[3.0]},
    "beamwidth":2.0,
    "frequency": 450e6,
    "snrlimit": 4.0
}

fylingdale = {
    "name":"fylingdale",
    "loopgain": 310,
    "location": {"lat":57.6, "lon":-4.5, "heightM":10},
    "fence":{"az":[0, 360],"el":[3.0]},
    "beamwidth":2.0,
    "frequency": 450e6,
    "snrlimit": 4.0
}


almond = {
    "name":"almond",
    "RCSData": {"450":{"url":"C:\\Users\\Jerem\\Downloads\\AOC_az_el_450MHz_pencil_almond_half_deg.xlsx","sheetname":"almond","frequency":450e6},
                "449.5":{"url":"C:\\Users\\Jerem\\Downloads\\almond_40_rcs_4495_4505_460.xlsx","sheetname":"449_5","frequency":449.5e6},
                "450.5":{"url":"C:\\Users\\Jerem\\Downloads\\almond_40_rcs_4495_4505_460.xlsx","sheetname":"450_5","frequency":450.5e6},
                "460":{"url":"C:\\Users\\Jerem\\Downloads\\almond_40_rcs_4495_4505_460.xlsx","sheetname":"460","frequency":460e6}},
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

pencil = {
    "name":"pencil",
    "RCSData": {"450":{"url":"C:\\Users\\Jerem\\Downloads\\AOC_az_el_450MHz_pencil_almond_half_deg.xlsx","sheetname":"pencil","frequency":450e6}},
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

objects = {"x29":x29,"tcone":tcone,"tcone2":tcone2,"pencil":pencil,"almond":almond}
sensors = {"cali":cali, "hawaii": hawaii, "cape cod":cape_cod, "thule":thule,"fylingdale":fylingdale}
simulation = {"start time":"2025-01-01T01:01:00.000Z", "stop time":"2025-01-01T01:51:00.000Z","time step":1.0}