import sys
import os

home_folder = "/apps/tibco/SSL_CHECK/"
input_folder = home_folder+"input/"
output_folder = home_folder+"output/"
limit_days = 30

os.system("rm -rf "+output_folder+"report.html")


def check_dates(url):
        #print url
	server = url.replace('https://','')
	#print server
	nlb = os.popen("nslookup "+server+"|grep \"canonical name\"|sed -e 's/.*=\s//'").read()
	nlb = nlb.rstrip()
	#print nlb
	expiry_date = os.popen('echo |openssl s_client -servername '+server+' -connect '+server+':443 2>/dev/null | openssl x509 -noout -dates|grep notAfter|sed -e s/notAfter=//').read()
	expiry_date = expiry_date.rstrip()
	posix_expiry_date = os.popen("date -d \""+expiry_date+"\" '+%s'").read()
	#print posix_expiry_date
	posix_current_date = os.popen("date  '+%s'").read()
	#print posix_current_date
	
	diff_days = ((int(posix_expiry_date) - int(posix_current_date)) / 24 / 3600)
	#print (diff_days)

	if ( diff_days < limit_days ):
		#print "Certificate for "+url+" will expire in less than "+str(diff_days)+" days"
		#print "<tr><td>"+url+"</td><td>"+nlb+"</td><td>"+server+"</td><td>"+expiry_date+"</td></tr>"
		message1 = "<tr><td>"+url+"</td><td>"+nlb+"</td><td>"+server+"</td><td>"+expiry_date+"</td></tr>"
		htmlwriter.write(message1)


#########HTML PART 1####################

htmlwriter = open(output_folder+"/report.html","w")

message = """
<!DOCTYPE html>
<html>
<head>
<style>
table {
    width:100%;
}
table, th, td {
    border: 1px solid black;
    border-collapse: collapse;
}
th, td {
    padding: 15px;
    text-align: left;
}
table#t01 tr:nth-child(even) {
    background-color: #eee;
}
table#t01 tr:nth-child(odd) {
   background-color: #fff;
}
table#t01 th {
    background-color: black;
    color: white;
}
</style>
</head>
<body>

<h2 Align=center><font size=25 color="#006400">SSL CERTIFICATE REPORT</h2>
<table id="t01">
  <tr>
    <th>URL</th>
    <th>NLB</th> 
    <th>DNS</th>
    <th>End Date</th>
  </tr>

"""


htmlwriter.write(message)

with open(input_folder+"urls.input") as urls:
	for line in urls:
		line = line.rstrip()
		if not line.startswith('#'):
			check_dates(line)	


########HTML PART 2##########

message2 = """
</table>

</body>
</html>
"""

htmlwriter.write(message2)

htmlwriter.close()


os.system("/apps/tibco/SSL_CHECK/SendMail.sh")
