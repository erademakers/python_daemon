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
