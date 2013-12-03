#!/bin/bash
#arguments should be: 1)hostname, 2)port#, 3)seconds to move, 4)language_implementer (ex: python, clisp, java, <nothing for c>), 5)program name
mkfifo mypipe
cat mypipe|nc -w $3 $1 $2|$4 $5
echo timeout or win
rm -f mypipe
