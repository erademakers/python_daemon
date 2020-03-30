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
    'RR': -1,
    'VT': -1,
    'PK': -1,
    'TS': -1,
    'IE': -1,
    'PP': -1,
    'ADPK': -1,
    'ADVT': -1,
    'ADPP': -1,
    'MODE': -1
}

def compute_LRC(bytes):
    checksum = 0
    for byte in bytes:
        checksum ^= byte

    return checksum


def construct_serial_message(key, val):
    line = key + "=" + str(val) + "="
    line = line.encode('utf-8')
    checksum = compute_LRC(line)
    return {'type': key, 'val': val, 'checksum': checksum}
