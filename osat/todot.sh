grep -n ".*TODO:" ./osa2.tex | sed 's/%/ /' |sed 's/^/- /' > ../TODO.md 
