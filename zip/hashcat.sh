#!/bin/bash
./hashcat-7.1.2/hashcat.bin -m 17225 tmp.hash -a 3 -1 ?l?d --increment --increment-min 4 --increment-max 6 ?1?1?1?1?1?1 --outfile-format 2 -D 1 --quiet
