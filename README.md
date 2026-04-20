# RISC-V-HPC-Life

- Tenemos 3 postes :
                *A = Origen
                * B = Auxiliar
                * C = Destino
- N discos

Al inicio todos los discos estan apilados en el disco A. ordenados de mayor a menor. (el mas grande abajo, el mas pequeno arriba)
Mover toda la torre al poste C utilizando el poste B como auxiliar, tomado en cuenta estas 3 reglas estrictamente.

1. Unidad              : Solo se puede mover un disco a la vez
2. Disponibilidad      : Solo puedes mover el disco que este en la cima de cualquier pila.
3. Gravedad Estructural: Jamas se puede poner un disco mas grande sobre un disco mas pequeño.

Con estas reglas para desoxidar un poco la ingenieria vamos a tratar de describir lo anterior de una manera matematica :).

Para modelar esto, no pensamos en mover los discos individuales si no mover "sub-torres".

- Sea T(N) el numero exacto de movimientos necesarios para transladar una torre de N discos.

 Para mover el disco mas grande (el disco N) de origen a destino, obligatoriamente debemos quitar N-1 discos que tiene encima
 y ponerlos temporalmente en el poste auxiliar.

 Podemos deducir una ecuacion de Recurrencia:

                                    T(N) = T(N - 1 ) + 1 + T(N - 1)
Agrupando los terminos tenemos:
                                T(N) = 2T(N-1) + 1

Si queremos desglosar la ecuacion:
            - T(N - 1): Movimientos para pasar la sub-torre de encima hacia el poste auxiliar
            - +1      : El movimiento atomico del disco gigante desde origen --> destino
            - T(N - 1): Movimiento para traer la sub-torre desde el auxiliar hacia el destino final. poniendolo sobre el disco      gigante.

## Caso base

Si solo hay un disco N = 1, simplemente lo movemos :

                T(1) = 1

Resolviendo la ecuacion:

                T(N) = 2 T(N-1) + 1                entonces | T(N - 1) = 2T(N-2) + 1 
                     = 2(2T(N - 2) + 1) + 1 
                     = 2^2 T (N - 2) + 2 + 1       entonces | T(N - 2) = 2T(N-3) + 1  
                
                     = 2^2 (2T(N-3) + 1) + 2 + 1
                     = 2^3 T(N-3) + 2^2 + 2 + 1    entonces | 2 = 2^1 and 1 = 2^0

                     = 2^3 T (N - 3) + 2^2 + 2^1 + 2^0

Entonces podemos  
