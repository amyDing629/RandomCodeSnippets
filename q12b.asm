.globl q12

.data
len:    .word   6
list:   .word   -3, 2, 0, -1, 4, -5

.text
q12:
    la $s0, list    
    la $s1, len
    li $t1, 0
    lw $t3, 0($s1)
mainLoop:
    beq $t1, $t3, done #exit loop if reach the end of the list
    lw $t2, 0($s0) #load value
    mul $t2, $t2, 16
    sw $t2, 0($s0) #set new value
    addi $s0, $s0, 4 
    addi $t1, $t1, 1
    j mainLoop
    
done:
    addi $s0, $s0, -24
    
    #uncomment the following code to print new list values
    
    #li $t1, 0
    #Loop:
    #beq $t1, $t3, end
    #lw $t2, 0($s0)
    #li $v0, 1
    #move $a0, $t2
    #syscall
    #addi $s0, $s0, 4
    #addi $t1, $t1, 1
    #j Loop
    #end:
    li $v0, 10              
    syscall 
    



