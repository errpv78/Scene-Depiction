# Scene-Depiction
Scene Depiction in Videos for blind by Image Captioning

## Developer Instructions
1. If virtualenv not installed, then install it either depending on your system or by:<br>
<code>pip install virtualenv</code><br>

2. Create virtualenv<br>
<code>virtualenv cap </code>
  
3. Always work in cap virtualenv: Activate virtualenv by following command in terminal<br>
<code>source cap/bin/activate</code> 

4. If a new library is to be installed while working, install it then, before commiting update requirements.txt by:<br>
<code>pip freeze > requirements.txt </code>

5. If in case some requirements are not met while running code: 1. Run 4th command, then run:<br>
<code>pip install -r requirements.txt</code>

6. Before committing cut and past the virtualenv folder named as cap out of project folder, then commit and push otherwise it would be too heavy to push.<br>
After successfully committing again move the cap folder back into project folder.
