.globl q12

.data
len:    .word   6
list:   .word   -3, 2, 0, -1, 4, -5

.text
q12:
    la $s0, list    
    la $s1, len
    
    li $t1, 0
    li $t2, 0
    addi $t6, $zero, 1
    addi $t5, $zero, 4
    lw $t3, 0($s1)


    mainLoop:
    beq $t1, $t3, done #exit loop if reach the end of the list
    sub $t4, $t3, $t1
    subi $t4, $t4, 1
    
    addi $s0, $s0, 4 
    addi $t1, $t1, 1
    j mainLoop
    
    jal swapOnce
    returnMain:
    
    li $v0, 10
    syscall


swapOnce:
        secondLoop:
        beq $t7, $t6, done2
        lw $t8, list($t2)
        lw $t9, 0($t3)
        bgt $t8, $t9, exchange
        exchangeDone:
        addi $t7, $t7, 1
        j secondLoop
        done2:
        addi $s0, $s0, 4
        j returnMain
done:
    addi $s0, $s0, -24
    li $t1, 0
    #uncomment the following code to print new list values
    jal print
    li $v0, 10              
    syscall 
    
 
  print:
    li $t1, 0
    Loop:
    beq $t1, 6, end
    lw $t2, 0($s0)
    li $v0, 1
    move $a0, $t2
    syscall
    addi $s0, $s0, 4
    addi $t1, $t1, 1
    j Loop  
    end:
    addi $s0, $s0, -24
    jr $ra         
    

