"""
Settings definition for ventilator
"""

alarm ="ALARM"

measurements = ['BPM',  # Breaths per minute
                'VOL',  # Volume
                'TRIG', # Trigger
                'PRES'  # Pressure
]

settings = ['RR',   # Respiratory rate
            'VT',   # Tidal Volume
            'PK',   # Peak Pressure
            'TS',  # Breath Trigger Threshold
            'IE',   # Inspiration/Expiration (N for 1/N)
            'PP',   # PEEP (positive end expiratory pressure)
            'ADPK', # Allowed deviation Peak Pressure
            'ADVT', # Allowed deviation Tidal Volume
            'ADPP', # Allowed deviation PEEP
            'MODE'  # Machine Mode (Volume Control / Pressure Control)
]

settings_values = {
    'RR': 0,
    'VT': 0,
    'PK': 0,
    'TS': 0,
    'IE': 0,
    'PP': 0,
    'ADPK': 0,
    'ADVT': 0,
    'ADPP': 0,
    'MODE': 0
}

def compute_LRC(bytes):
    checksum = 0
    for byte in bytes:
        checksum ^= byte

    return checksum


def construct_serial_message(key, val):
    line = key + "=" + str(key) + "="
    line = line.encode('utf-8')
    checksum = compute_LRC(line)
    return {'type': key, 'val': val, 'checksum': checksum}
