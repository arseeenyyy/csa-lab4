: cat
    begin
       key \ comment section 1
       dup 
       emit \ comment section 2
    0 = until ( comment section 3 )
;
cat
: cat2
    dup 
    dup 
    drop 
    drop
;
cat2 
