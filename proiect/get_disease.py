import cgi
form = cgi.FieldStorage()
disease = form.getvalue('disease')
symptom = form.getvalue('symptom')

return disease + ' ' + symptom
