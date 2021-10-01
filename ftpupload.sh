#!/bin/bash


mv flights_data.txt flights_data

ftp_user="qt1"
ftp_pass='YpMePUXK'
ftp_ip="192.168.255.253"
ftp_port=21
ftp_file_to_upload="flights_data"
ftp_file_destiny="Web/Hotel-Telecable"

ftp -inv <<EOF
open $ftp_ip $ftp_port
user $ftp_user $ftp_pass
cd $ftp_file_destiny
mdelete $ftp_file_to_upload
mput $ftp_file_to_upload
close 
bye
EOF

