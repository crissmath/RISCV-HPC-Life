#!/bin/bash


#counter
cnt_steps=0


# first arg : N_disks, default_value = 3
N_DISKS=${1:-3}  


# print function
print_mov(){
    local disk=$1
    local source=$2
    local target=$3

    ((cnt_steps++))

    printf "[Step %02d] (Disk %d): \e[1;32m%s\e[0m --> \e[1;34m%s\e[0m\n" \
    "$cnt_steps" "$disk" "$source" "$target"  

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
echo "================================================================"
echo "                   TOWER OF HANOI                               "
echo "================================================================"
echo "Config: $N_DISKS disks      |      System: $(uname -s)/$(uname -m)"
echo "----------------------------------------------------------------"
solve_hanoi "$N_DISKS" "P_A" "P_B" "P_C"
echo "--------------------------------------------------------------"
echo " Simulation completed in $cnt_steps steps."
echo "--------------------------------------------------------------"
echo "================================================================"
