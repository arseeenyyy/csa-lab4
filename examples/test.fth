: main
    10 20 +
    dup *
;
: main2
    dup dup drop drop
    x y
;
variable x 
variable y

main  
main2
halt