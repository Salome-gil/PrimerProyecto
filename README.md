# PrimerProyecto
Primer 20% Programación de Software
<hr>

### 1.  Enunciado
Se desea crear un sitio web que permita realizar Préstamos Bibliotecarios. El sitio interactúa con clientes (estudiante, empleados y profesores) y con usuarios (organizador o bibliotecario y administrador). Los clientes vía WEB pueden consultar préstamos, material bibliográfico en mora e historial de préstamos, renovar préstamo y reservar material bibliográfico. El Bibliotecario puede realizar préstamos, consultar material disponible, consultar libros más prestados, consultar prestamos atrasados, además actualiza el estado físico de los libros y genera un informe diario de cantidad de libros prestados y en mora.

### Prestar Material bibliográfico: 
- Al momento de realizar un préstamo el cliente llega donde el bibliotecario con el libro a prestar. A continuación, el bibliotecario ingresa el código del cliente (Carnet si es estudiante y  cédula si es empleado o docente) y el código del libro con lector de código de barras, posteriormente el sistema valida que el cliente exista, que el material bibliográfico exista y su estado sea disponible, una vez todas las condiciones se cumplen el sistema procede a realizar el préstamo, dentro de este proceso se cambia el estado del material bibliográfico de disponible a no disponible y aparece un mensaje indicando que el préstamo fue realizado  exitosamente con los datos del cliente(carnet o cédula según sea el caso),  la fecha de préstamo y la fecha de  entrega. 
- En caso de que el código del cliente no exista o el material bibliográfico no esté disponible, el sistema arroja un mensaje correspondiente a la inconsistencia indicando que no es posible realizar el préstamo.
- En caso de que el material bibliográfico haya sido reservado por otro cliente el préstamo no se puede realizar.

### Renovar Préstamo: 
- El cliente se acerca al bibliotecario con un material bibliográfico que desea renovar el préstamo, el bibliotecario debe validar que el préstamo exista y que el cliente si sea el que tiene en préstamo el material bibliográfico, también debe verificar que éste no se encuentre reservado para la fecha que requiere el cliente la renovación. 
- En caso de poder realizarse la renovación se debe cambiar en el préstamo la fecha de entrega por la nueva fecha, y actualizar el estado del material bibliográfico a “No disponible”. 
- Si el cliente no es el mismo que aparece en el préstamo, el bibliotecario cancela la renovación e informa al cliente. 
- Si el código del material bibliográfico no es válido, se imprime un mensaje “El código del material bibliográfico no se encuentra en el sistema”.
- Según las normas de la institución no se pueden renovar ni prestar materiales bibliográficos si estos se encuentran reservados, además todo préstamo se debe conservar, y las renovaciones deben actualizar la fecha de entrega del préstamo. 
- Para renovar un préstamo, el día en que termina el préstamo el cliente puede diligenciar la renovación solo si el material no ha sido reservado para esa fecha de entrega. De forma presencial el recepcionista pide al cliente el código del cliente, el código del material bibliográfico y la nueva fecha de entrega y lo renueva. O vía web el cliente ingresa la nueva fecha de entrega y lo renueva. 

### Devolver material bibliográfico: 
- El estudiante entrega el material bibliográfico, el bibliotecario ingresa los datos del material bibliográfico, verifica si el préstamo existe, luego verifica que el material bibliográfico sea ingresado antes o en la fecha indicada para luego cancelar el préstamo. Por último, actualiza el estado del material bibliográfico.

### Cancelación de reserva: 
- Es similar a la opción de reserva. Vía web, el cliente consulta con el código del material bibliográfico la reserva y se cancela


<hr>

## Equipo de Trabajo
#### Maria Fernanda Palacio Agudelo
#### Salome Gil Chanci