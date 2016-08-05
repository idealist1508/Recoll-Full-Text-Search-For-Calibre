from subprocess import Popen, PIPE, STDOUT
import re

text = 'wpf'
cmd = ['C:/Program Files (x86)/Recoll/recoll', '-c', 'c:/Users/spolonski/AppData/Roaming/calibre/plugins/recollFullTextSearchPlugin', '-b', '-t', text]
#cmd2 = "recollindex -c /home/stanislav/recollplugin -z"
p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
output = p.stdout.read()
#print "work"
#p.wait()
print output
try:
    found = re.findall(r" \((\d+)\)\/", output)
    
    #found = re.findall(r"\((\d+)\)\/", "file:///home/stanislav/Calibre Library/Doina Logofatu/Algorithmen und Problemlsungen mit C___ Von der Diskreten Mathematik zum fertigen Programm - Lern- u (61)/Algorithmen und Problemlsungen mit C___ Von der Diskreten Mathematik zum fertigen Programm - Lern- u - Doina Logofatu.pdf file:///home/stanislav/Calibre Library/Dietrich May/Grundkurs Software-Entwicklung mit C___ Praxisorientierte Einfuhrung mit Beispielen und Aufgaben - E (62)/Grundkurs Software-Entwicklung mit C___ Praxisorientierte Einfuhrung mit Beispielen und Aufgaben - E - Dietrich May.pdf")#file 123 (22)/ sdf (123)/ sdf
except AttributeError:
    # AAA, ZZZ not found in the original string
    found = '' # apply your error handling
wholeString = '#cid:'
if len(found) != 0 :
    for elem in found:
        wholeString += '=' + elem + ' or '
        print elem
wholeString = wholeString[:-4]

print wholeString
print found
print(len(found))
