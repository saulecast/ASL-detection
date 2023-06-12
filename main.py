import ModoControlADistancia as control_a_distancia

def Fcontrol_a_distancia(self):
    print("presiona 'D' para detener este modo")
    print("presiona la tecla d cuando quieras detener este modo")
    
    try:
        control_a_distancia()
    except TypeError as err:
        print (err)
        print("modo de control a distancia desactivado")  

if __name__ == "__main__":
    Fcontrol_a_distancia()
