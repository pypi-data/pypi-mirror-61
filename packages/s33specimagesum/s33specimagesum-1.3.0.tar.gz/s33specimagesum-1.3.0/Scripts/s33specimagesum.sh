#! /bin/bash
if [ -f "$HOME/Anaconda3/bin/python" ]; then
	ANACONDA_LOCATION="$HOME/Anaconda3"
elif [ -f "$HOME/anaconda3/python" ]; then
	ANACONDA_LOCATION="$HOME/anaconda3"
elif [ -f "$HOME/opt/anaconda3/python" ]; then
	ANACONDA_LOCATION="$HOME/opt/anaconda3"
elif [ -f "/opt/anaconda3/python" ]; then
	ANACONDA_LOCATION="/opt/anaconda3"
elif [ -f "$HOME/opt/Anaconda3/python" ]; then
	ANACONDA_LOCATION="$HOME/opt/Anaconda3"
elif [ -f "/opt/Anaconda3/python" ]; then
	ANACONDA_LOCATION="/opt/Anaconda3"
elif [ -f "/APSshare/anaconda3/x86_64/bin/python" ]; then
	ANACONDA_LOCATION=/APSshare/anaconda3/x86_64
else 
	echo "Cannot find Anaconda Python"
	exit 1
fi
source $ANACONDA_LOCATION/bin/activate

conda activate s33specimagesum

python -m s33specimagesum