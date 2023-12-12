# Online-Booking-System

### 🧑🏽‍💻 Here is a workflow to contribute to projects.

1. Clone this repository to your local machine.

```
git clone [this-repo]
```

2. Change to the repository directory on your computer:

```
cd Online-Booking-System
```

3. Change to dev branch as the template for your new branch:

```bash
git checkout dev
```

4. Create a branch using the `git checkout` command:

```bash
git checkout -B branch-name
```

5. Create your virtual environment(Linux OS)

```bash
python3 -m venv venv; source venv/bin/activate
```

6. Install all Packages in requirements

```bash
pip install -r requirements.txt
```

7. Implementing your features
   if you install a new packge, add to the requirements file using this

```bash
pip freeze > requirements.txt
```

8. Run your code with this, ensure that is no error, if there is(are) errors, fix them before pushing

```bash
gunicorn --config gunicorn-cfg.py run:app
```

or

```bash
gunicorn --config gunicorn-cfg.py --access-logfile access_log.log --error-logfile error_log.log run:app
```

5. Push to your branch(not main branch)

```bash
git push origin  branch-name
```

6. Then Come to Github to make pull request
