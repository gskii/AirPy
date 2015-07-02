import threading
import time
import algorithm

class Airplane(object):
    '''
    Airplane class.
    Предназначен для хранения промежуточной информации и организации вычислений координат.
    Метод calculateCoordinates спроектирован для работы в отдельном потоке.
    По сути, является перемычкой между GUI и Algorithm.
    '''
    
    def __init__(self, name, algorithm, **kwargs):

        # Основные системные объекты
        self.lock = threading.Lock()        # Для соблюдения очередности пользования
        self.alg  = algorithm               # Обязателен для организации вычислений
        self.name = name
        self.live = True                                                              
       
        # Координатные переменные
        self.lat     = kwargs.setdefault('x', (0,0,0))      # Широта         
        self.lon     = kwargs.setdefault('y', (0,0,0))      # Долгота
        self.latType = 0                                    # 0 - С.Ш. / 1 - Ю.Ш.
        self.lonType = 0                                    # 0 - В.Д. / 1 - З.Д.
        self.dest    = kwargs.setdefault('dest', (0,0,0))   # Направление
        self.speed   = kwargs.setdefault('speed', 0.)

        # Работа с файлом
        self.path    = kwargs.setdefault('path', 'test.txt')
        try:
            self.file = open(self.path, 'wt')
        except:
            print('File for', self.name, 'is not created!')
            
    def calculateCoordinates(self):
        '''
        Предназначен для работы в отдельном потоке, метод не следует вызывать явно.
        Вызов должен иметь вид:
            threading.Thread(target = Airplane.calculateCoordinates, args = [AirplaneObj])
        Организует логику вычислений.
        '''
        while(self.live):                             
            try:
                beginTime = time.time()                 
                self.lock.acquire(True)                 # Заблокировали доступ к данным
                
                matrix = algorithm.Algorithm.start( alg,
                    self.lat[0], self.lat[1], self.lat[2],
                    self.lon[0], self.lon[1], self.lon[2],
                    self.dest[0], self.dest[1], self.dest[2],
                    self.speed)
                
                self.lat = matrix[0]
                self.lon = matrix[1]
            except:
               print('[oops, some error...]')
            finally:
                self.lock.release()                     # Высвободили данные
                self.saveCoordinates()                  
                endTime = time.time() - beginTime       # Время окончания вычислений
                waitTime = 1.0 - endTime                # Время до следующей итерации 
                if (waitTime > 0): time.sleep(waitTime) 
                else: print('[WARNING] too long calculations!\n')    
    
    def saveCoordinates(self):
        #X:(0, 0, 0) [ЮШ]     Y:(0, 0, 0) [ЗД]	Курс:(0, 0, 0)	Скорость: 0 км/ч      Высота: 0 км
        if self.file:
            msg = str(self.lat)
            if self.latType:
                msg += ' [ЮШ]\t'
            else:
                msg += ' [CШ]\t'
            msg += str(self.lon)
            if self.lonType:
                msg += ' [ВД]\t'
            else:
                msg += ' [ЗД]\t'
            msg += '\n'
            self.file.write(msg)


if __name__ == '__main__':

    alg = algorithm.Algorithm()
    a1 = Airplane('test', alg, path = '1.txt', dest = (12,1,1), speed = 20000.)
    t1 = threading.Thread(target = Airplane.calculateCoordinates, args = [a1])
    t1.start()
    t1.join(2)
    a1.live = False
    del a1

    
