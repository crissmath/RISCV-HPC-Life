!/usr/bin/bash


#counter
cnt_steps=0

# print function
print_mov(){
    local disk=$1
    local source=$2
    local target=$3

    ((cnt_steps++))

    printf "[Step %02d]" "$cnt_steps"

}





## Recursion demostration
solve_hanoi(){
    local n=$1
    local source=$2
    local aux=$3
    local target=$4

    # Base case : 1 disk
    if[ "$n" -eq 1 ]; then
        print_move 1 "$source" "$target"

}
