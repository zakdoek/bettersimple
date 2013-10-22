echo "starting deployment"
s3cmd sync /home/schillingt/Dropbox/Projects/bettersimple/static/ s3://better-simple
git add .
git commit -m "$1"
git push heroku master
echo "finished"
