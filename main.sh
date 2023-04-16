#!/bin/bash 


# Abrir una nueva terminal y ejecutar worker.py
gnome-terminal -- bash -c "python3 worker.py; exec bash"
gnome-terminal -- bash -c "python3 worker.py; exec bash"


# Ejecutar el bucle
for i in {1..100}
do 
    python3 wellnessSensor.py
    python3 pollutionSensor.py
done

# Abrir una nueva terminal y ejecutar terminal.py
gnome-terminal -- bash -c "python3 terminal.py; exec bash"
gnome-terminal -- bash -c "python3 terminal.py; exec bash"


# Abrir una nueva terminal y ejecutar MeteoProxy.py
gnome-terminal -- bash -c "python3 meteo_proxy.py; exec bash"
