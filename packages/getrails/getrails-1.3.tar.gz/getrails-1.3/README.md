<center>
  <img src="img/beta1.jpg" alt="Getrails" width="900px"/>
</center>

# GETRAILS
Lib of OSINT and Dork hacking that work with Google and Duckduckgo

# Use

```python
import getrails
getrails.search('site:scanme.nmap.org')) # Try Google search if return error use Duckduckgo
# ["http://scanme.nmap.org",...]

getrails.go_gle("term") # Searching Google
getrails.go_duck("term") # Searching Duckduckgo
```

# Install

```python
pip3 install getrails
```
