from datetime import datetime, timedelta



class MyTime:
    """ Define el día y horas actuales. Puedes alternar entre usar el tiempo actual o un tiempo estático personalizado (para fines de debug). """
    _use_now = True
    _custom_datetime = None
    
    @classmethod
    def is_automatic(cls) -> bool:
        """ Devuelve True si se debe usar la fecha y hora actuales, False si se debe usar una fecha y hora personalizada. """
        return cls._use_now or cls._custom_datetime is None

    @classmethod
    def get(cls) -> datetime:
        """ Devuelve la fecha y hora actuales según la configuración realizada con ``set()``. """
        if cls.is_automatic():
            now = datetime.now()
            now += timedelta(hours=1) # Añadimos una hora para que coincida con la hora de España
            return now

        return cls._custom_datetime
    
    @classmethod
    def set(cls, use_now, custom_date=None, custom_time=None):
        """ Configura si se debe usar la fecha y hora actuales o una fecha y hora personalizada. """
        cls._use_now = use_now
        if not use_now and custom_date and custom_time:
            cls._custom_datetime = datetime.combine(custom_date, custom_time)