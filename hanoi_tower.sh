#!/bin/bash
#counter
cnt_steps=0

# print function
print_mov(){
    local disk=$1
    local source=$2
    local target=$3

    ((cnt_steps++))

    printf "[Step %02d] (mov disk %d) %s --> %s \n" "$cnt_steps" "$disk" "$source" "$target"  

}

## Recursion demostration
solve_hanoi(){
    local n=$1
    local source=$2
    local aux=$3
    local target=$4

    # Base case : T(1) = 1
    if [ "$n" -eq 1 ]; then
        print_mov 1 "$source" "$target"
        #echo "Hola 1"
    else

        # call 1: Move top n-1  disk from Source --> Auxiliar
        solve_hanoi $((n - 1)) "$source" "$target" "$aux"

        # show work 
        print_mov "$n" "$source" "$target"

        # call 2: Mov the n-1 disk from Auxiliar --> Target
        solve_hanoi $((n - 1)) "$aux" "$source" "$target"
    fi
}




## Main
clear 
echo Tower of hanoi

N_DISKS=5


echo "Start Simulation $N_DISKS ..."
solve_hanoi "$N_DISKS" "P_A" "P_B" "P_C"

echo "end simulation ..."