from datetime import datetime



class MyTime:
    """ Define el día y horas actuales. Puedes alternar entre usar el tiempo actual o un tiempo estático personalizado (para fines de debug). """
    _use_now = True
    _custom_datetime = None
    
    @classmethod
    def get(cls) -> datetime:
        if cls._use_now or cls._custom_datetime is None:
            now = datetime.now()
            now.hour += 1 # Añadimos una hora para que coincida con la hora de España
            return now

        return cls._custom_datetime
    
    @classmethod
    def set(cls, use_now, custom_date=None, custom_time=None):
        cls._use_now = use_now
        if not use_now and custom_date and custom_time:
            cls._custom_datetime = datetime.combine(custom_date, custom_time)