scp -p -r * zue84905@dsastv003.dl.ac.uk:~/CAS_test
ssh zue84905@dsastv003.dl.ac.uk 'cd ~/CAS_test; docker stop $(docker ps -q --filter ancestor=cas-server ); chmod +x ./build.sh; ./build.sh'
ssh zue84905@dsastv003.dl.ac.uk 'docker run -p 5000:5000 -d cas-server'
python .\test\test_client.py dsastv003.dl.ac.uk
ssh zue84905@dsastv003.dl.ac.uk 'docker stop $(docker ps -q --filter ancestor=cas-server )'
