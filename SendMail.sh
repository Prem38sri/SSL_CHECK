#!/bin/bash

# some variables
# refactoring the script such that all these values are
# passed from the outside as arguments should be easy

 (
                echo To: GAHS.EAI@accenture.com
                echo Cc: Mustapha.Hachaichi@sanofi.com,v.narasimha.bathala@accenture.com
                echo From: EAI.Admin@Sanofi.com
                echo "Content-Type: text/html;"
                echo Subject: "TIBCO ADMIN NLB CERTIFICATE EXPIRY REPORT"
                cat /apps/tibco/SSL_CHECK/output/report.html
                ) | /usr/sbin/sendmail -t

