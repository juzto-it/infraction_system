from datetime import datetime
import pytz
class Formatter:

    @staticmethod
    def format_date_verifik(c_date: str) -> str:
        
        try:
            
            if '/' in c_date:
                new_date = c_date.replace('/', '-')
                return new_date
            else:
                new_date = c_date[0:4] + '-'+ c_date[4:6] + '-' + c_date[6:]
                return new_date
            
        except Exception as _e:
            return c_date
            
    
    @staticmethod
    def clean_null_keys(exp: dict) -> dict:
        
        try:
            return {k:v for k, v in exp.items() if v is not None}
        except:
            return None


    @staticmethod
    def datetime_utc_now():
        
        time_zone = pytz.timezone('America/Bogota')
        dt = datetime.now(time_zone)
        dt = dt.strftime('%Y-%m-%d %H:%M:%S')
        return str(dt)