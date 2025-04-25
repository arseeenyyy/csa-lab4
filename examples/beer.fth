: newline 10 emit ;

: beer dup . ." bottles of beer on the wall, " newline 
dup . ." bottles of beer" newline 
." takes one down, pass it around," 
newline 1 - dup . ." bottles of beer on the wall!" 
newline newline ; 

: song 100 1 do beer loop ; 
99 song