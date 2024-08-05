TO USE MYSQLI.py use this commnd 

python3 MYSQLI.py -l urls.txt -o save.txt
cat save.txt|httpx -mc 200|tee live.txt

TO USE LFI.py use this command 

python3 MYLFI.py -l urls.txt -o save.txt
cat save.txt|httpx -mc 200|tee live.txt
nuclei -l live.txt -t fuzz -tags lfi -dast
