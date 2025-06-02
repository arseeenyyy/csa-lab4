variable x 
variable y

: main
    10 20 +
    dup *
;
: main2
    dup dup drop drop
    x y
;
0 x !
0 y !
halt
