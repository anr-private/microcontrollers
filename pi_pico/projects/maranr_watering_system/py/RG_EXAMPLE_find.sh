RG_EXAMPLE_find.sh

rg -g '*.py' -g '!py/unit_tests/**' -F -e 'X.' py/
  -g XXXXX    glob
  -e PPPPP    specify the pattern
  -F          the pattern is literal not a regex
  py/         path is always at the end

If you omit -e, then the pattern PPP is the first 'bare' arg
and the path is the second 'bare' arg.


rg -n 'MwsWifi.get_ip_and_port' . --glob '!unit_tests/**'

###

