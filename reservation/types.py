TRIP = 0
APPOINTMENT = 1

def to_string(value):
    return {
        TRIP: 'Trip',
        APPOINTMENT: 'Appointment',
    }[value]

reservation_types = [(0, to_string(0)), 
    (1, to_string(1)),]
    
reservation_types_sorted = sorted(reservation_types,key= lambda rtype: rtype[1])
