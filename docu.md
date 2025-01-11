crontab -e
*/1 * * * * /website_tracker/script_hsbi.py  /website_tracker/script_hsbi.py > /website_tracker/script_hsbi.log 2>&1

*/1 * * * * source /programming_projects/website_tracker/venv/bin/activate && python3 /programming_projects/website_tracker/script.py > /programming_projects/website_tracker/script_hsbi.log 2>&1

*/1 * * * * source /Users/viktoriia/Desktop/programming_projects/website_tracker/venv/bin/activate && python3 /Users/viktoriia/Desktop/programming_projects/website_tracker/script_hsbi.py > /Users/viktoriia/Desktop/programming_projects/website_tracker/script_hsbi.log 2>&1

*/1 * * * * echo "Cron job started at $(date)" >> /Users/viktoriia/Desktop/programming_projects/website_tracker/debug.log && source /Users/viktoriia/Desktop/programming_projects/website_tracker/venv/bin/activate && echo "Virtual environment activated at $(date)" >> /Users/viktoriia/Desktop/programming_projects/website_tracker/debug.log && python3 /Users/viktoriia/Desktop/programming_projects/website_tracker/script_hsbi.py >> /Users/viktoriia/Desktop/programming_projects/website_tracker/script_hsbi.log 2>&1 && echo "Script completed at $(date)" >> /Users/viktoriia/Desktop/programming_projects/website_tracker/debug.log

*/1 * * * * /bin/bash -c "source /Users/viktoriia/Desktop/programming_projects/website_tracker/venv/bin/activate && echo 'Virtual environment activated at $(date)' >> /Users/viktoriia/Desktop/programming_projects/website_tracker/debug.log && python3 /Users/viktoriia/Desktop/programming_projects/website_tracker/script_hsbi.py >> /Users/viktoriia/Desktop/programming_projects/website_tracker/script_hsbi.log 2>&1 && echo 'Script completed at $(date)' >> /Users/viktoriia/Desktop/programming_projects/website_tracker/debug.log"

*/5 * * * * /Users/viktoriia/Desktop/programming_projects/website_tracker/venv/bin/python /Users/viktoriia/Desktop/programming_projects/website_tracker/script_hsbi.py >> /Users/viktoriia/Desktop/programming_projects/website_tracker/script_hsbi.log 2>&1 && echo "Script completed at $(date)" >> /Users/viktoriia/Desktop/programming_projects/website_tracker/debug.log


:wq
crontab -l

/Users/viktoriia/Desktop/programming_projects/website_tracker/script.py