# Investigación sobre RAID

## ¿Qué es RAID?

RAID (Redundant Array of Independent Disks) es una tecnología que combina múltiples discos duros en una sola unidad lógica para mejorar el rendimiento, la capacidad de almacenamiento y/o la tolerancia a fallos.

## Niveles de RAID

### RAID 0 (Striping)
- **Ventaja:** Mayor velocidad.
- **Desventaja:** No ofrece redundancia; si un disco falla, se pierde toda la información.

### RAID 1 (Mirroring)
- **Ventaja:** Alta redundancia; los datos se duplican en dos discos.
- **Desventaja:** Solo se utiliza la mitad de la capacidad total.

### RAID 5 (Striping con Paridad)
- **Ventaja:** Equilibrio entre rendimiento y redundancia; requiere al menos 3 discos.
- **Desventaja:** Si falla más de un disco, se pierde la información.

### RAID 6 (Striping con Doble Paridad)
- **Ventaja:** Permite que fallen hasta dos discos sin pérdida de datos.
- **Desventaja:** Menor rendimiento de escritura comparado con RAID 5.

### RAID 10 (1+0)
- **Ventaja:** Combina velocidad y redundancia; requiere al menos 4 discos.
- **Desventaja:** Costoso en términos de capacidad.

## Usos Comunes

- **Servidores:** Para asegurar la disponibilidad y protección de datos.
- **Estaciones de trabajo:** Donde se requiere alto rendimiento.
- **Sistemas de almacenamiento:** Para grandes volúmenes de datos.

## Consideraciones

- RAID no reemplaza las copias de seguridad.
- La elección del nivel depende de las necesidades de rendimiento y seguridad.

## Referencias

- [RAID Explained](https://www.intel.com/content/www/us/en/support/articles/000005837/memory-and-storage.html)