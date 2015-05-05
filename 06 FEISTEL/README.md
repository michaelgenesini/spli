# SPLI
##### Sicurezza Progettazione Laboratorio Internet

# enable ftp server
sudo -s launchctl load -w /System/Library/LaunchDaemons/ftp.plist

# tshark command 
tshark -i en1 -V -T text > log.txt

# clean file
cat log.txt | grep 'FTP Data' > cleaned.txt

# tcpflo command
tcpflow -i en1 -B -C -D > tcpflow.txt