from datetime import datetime



def cal_logic(arrival, departure):
    # Get today's date
    today = datetime.now().date()
    
    # Check if arrival date is before today's date or departure date
    if arrival < today or arrival >= departure:
        return False
    else:
        return True
