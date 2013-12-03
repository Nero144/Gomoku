#!/bin/bash
#arguments should be: 1)port#, 2)seconds to move, 3)language_implementer (ex: python, clisp, java, <nothing for c>), 4)program name
mkfifo mypipe
cat mypipe|nc -w $2 -l $1|$3 $4
echo timeout or win
rm -f mypipe
