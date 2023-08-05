<center>
  <img src="https://raw.githubusercontent.com/Vault-Cyber-Security/getrails/lib/img/beta1.jpg" alt="Getrails" width="900px"/>
</center>

![Upload Python Package](https://github.com/Vault-Cyber-Security/getrails/workflows/Upload%20Python%20Package/badge.svg?branch=lib)

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
