: cat
    begin
       key \ comment section 1
       dup 
       emit \ comment section 2
    0 = until ( comment section 3 )
;
: cat2
    lit 25 
    dup dup
    drop 
    emit
;
cat
cat2
halt