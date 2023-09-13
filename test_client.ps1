.\run_updater.ps1
scp -p -r * zue84905@dsastv003.dl.ac.uk:~/CAS_test
ssh zue84905@dsastv003.dl.ac.uk 'cd ~/CAS_test; docker stop $(docker ps -q --filter ancestor=cas-server ); chmod +x ./build.sh; ./build.sh'
ssh zue84905@dsastv003.dl.ac.uk 'docker run -p 5000:5000 -d cas-server'
Start-Sleep -Seconds 5