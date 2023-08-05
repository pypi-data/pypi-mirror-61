
# pepperssh

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-generate-toc again -->
**Table of Contents**

- [pepperssh](#pepperssh)
    - [Files](#files)
        - [Using Files Remotely](#using-files-remotely)
        - [Templates](#templates)
    - [Utilities](#utilities)
        - [Shell](#shell)
        - [chdir](#chdir)
    - [Installation](#installation)
    - [How It Works](#how-it-works)
    - [Motivation](#motivation)

<!-- markdown-toc end -->


This is a library for extremely simple remote administration and deployment
using SSH.  It allows you to send a Python script to a remote host and execute
it.  You can also execute functions in the script individually.

``` python
from pepperssh.client import Client

client = Client('host.example.com')

# Send a local Python file to the remote host.  The script
# is executed and anything printed to the screen remotely
# is printed here.
script = client.script('dbutils.py')

# Call a specific function on the remote host.  Again, output
# to the screen is printed here.

result = script.resetdb(password=password)
```
    
## Files

### Using Files Remotely

One way to use local files on the remote host is to pass the local filename as a
parameter to a remote function, but wrap it in a File or Template object.  Under
the covers, the local file is copied to the remote host and the parameter name
is replaced with the remote filename.

In this example, we'll pass the "update.sql" file to a remote function named
"update".

``` python
from pepperssh.client import Client, File

client = Client('host.example.com')
script = client.script('dbutils.py')

script.update(File('update.sql'))
```
    
The "update.sql" file is copied to the host and the remote code will receive a
single string which is the fully qualified filename of the copied file.

``` python
def update(update_file):
    # At this point `update_file` is a string and is the path to the
    # file
    sql = open(update_file).read()
```

### Templates

The Template type is a subclass of File and works the same way.  However, it
also takes a mapping object and performs substitution on the file before copying
it.  Substitution is performed
using [str.format](https://docs.python.org/3/library/string.html#formatstrings).

> It seems very likely that this will be changed to use a more powerful template
> language like Jinja.  It would be ideal to find one that is backwards
> compatible instead of one use double braces.  Suggestions are welcome, but it
> will need to be a Python-only project so it can be easily pushed to remote
> hosts.

For example, if you had a file named "grant.sql" with the following contents:

``` sql
alter default privileges in schema public
grant select, insert, update, delete
on tables
to {dbuser};
```

You could send it to a remote function *and* replace "{dbuser}" with "admin"
using this code:

``` python
from papperssh.client import Template

vars = {'dbuser': 'admin'}
script.dogrant(Template('grant.sql', vars))
```

    
The remote dogrant function will receive just the filename of the processed
file.

There is also special handling of namedtuples, they are passed to str.format as
both a sequence and a dictionary (using `_asdict`).  This allows fields in the
tuple to be accessed by position ("{0}") but also by name ("{dbuser}") which is
considerably easier to maintain.

``` python
Host = namedtuple('Host', 'dbuser dbname password')

host = Host('admin', 'test', 'mypass')
script.dogrant(Template('grant.sql', host))
```

This will substitute the same "{dbuser}" as the dictionary example above.  (Also
note that str.format can be passed keys that are not in the file.  These values
are not put into the file and are not transferred to the remote host in any
way.)

## Utilities

This project is all about you writing your deploy scripts the way you want, in Python.
However, I will provide some generic utilities that I find useful.

### Shell

IMPORTANT: When running shell commands on the remote system, redirect stderr to
stdout or it may get sent back to the client incorrectly.  The
pepperssh.utils.shell function is provided to do this for youd:

``` python
from pepperssh.utils import shell

service = 'profitd'
shell(f'sudo systemctl start {service}')

shell(f"""
      ls -al /usr/local/bin
      rmdir /tmp/a
      """)
```

It is just a simple wrapper around `subprocess.run` that captures stdout and
stdin into the same stream and prints it to the Python stdout.  Unless
you disable the check, it will raise an exception if the command does not return
zero.

``` python
def shell(cmd, check=True):
    """
    Execute cmd.  Raises an exception if the command does not return 0
    """
    proc = subprocess.run(cmd, shell=True, check=False,
                          stderr=subprocess.STDOUT,
                          stdout=subprocess.PIPE)
    print(proc.stdout.decode('utf-8'))
    if check:
        proc.check_returncode()
```

> This is needed because currently stderr of a child process is not being captured
> in the Python process and is being sent back to the Client.  The Client and
> remote communicate using specially formatted messages, so "random" text will be
> printed to the screen and treated as a protocol error, stopping the script.

### chdir

This is a context manager that changes the directory to one you specify and then changes back
when the context is left:

``` python
from pepperssh.utils import chdir

print(os.getcwd())              # --> ~

with chdir('/usr/local/myproj')
    print(os.getcwd())          # --> /usr/local/myproj
    # ... do the work that
    # needs to be done in your
    # project directory

print(os.getcwd())              # --> ~
```

### archive

A function that creates a zip file based on a list of globs.

``` python
    archive('dist.zip', root='/my-project',
            exclude_dirs=['.git', '.venv', '__pycache__', '.mypy_cache',
                          'tmp', '.pytest_cache', 'tests'],
            patterns="""
                server1/*.py
                lib/**/*.py
                ! lib/secrets.py
            """)
```
    
## Installation

This package is all Python and can be installed with pip.  It is not yet on
pypi, so you'll need to give the GitLab URL:

``` shell
pip install https://gitlab.com/mkleehammer/pepperssh
```
    
It depends on the paramiko library to implement the SSH protocol:

``` shell
pip install paramiko==2.2.1
```

## How It Works

This project is in its infancy, so it is very simplistic.  For example, some
things it needs and will probably be added shortly:

* choosing the Python version (hardcoded to 3.6 right now)
* installing Python if it doesn't already exist (e.g. apt-get, etc.)
* installing requirements via pip for the remote script
* libraries for easily copying files that don't require a remote script

If you need these features sooner, please open
an [issue](https://gitlab.com/mkleehammer/pepperssh/issues).


The library currently works like so:

1. An SSH connection is created.
2. A temporary work directory is created on the remote host.  I'll refer to it
   as `rpath` (remote path).
3. The pepperssh package is transferred to the work directory `rpath/pepperssh`.
4. A small Python server is started which implements a REPL to receive commands,
   execute them, and return results.
5. When `client.script(filename)` is called, the script is copied to `rpath` and
   loaded as a module.  Any code in the module is executed and stdout is
   returned to the client.
6. When remote functions are called, parameters are pickled, the function is
   looked up by name by the remote server, and results are pickled and returned.
7. If a File or Template instance is passed as a parameter to a remote function,
   the file is first transferred to `rpath/files`, and the parameter is replaced
   with the remote files fully qualified name.

## Motivation

I have used a few remote administration projects, but have never found one that
was simple enough for small projects but trivial to extend.  Recently the extreme
frustration of spending two days trying to accomplish something that should be
simple was the last straw and pepperssh was born.

While I enjoy working with many languages, Python is extremely well suited for
administration work.  So I started with it as the base.

Static, declarative deployment files are often touted as being best for
maintainability, but they always ended up being a straight-jacket and cause more
work than they save.  After all, it is much easier to write maintainable Python
using embedded data structures than to write and maintain custom plugins for
each project.

Many tools obfuscate what they do behind plugins ("actions", "tasks", etc.) so
you need to dig through source.  Does the PostgreSQL grant plugin also update
defaults so new tables are accessible?  I plan on adding lots of utilites for
common tasks, but you can always use plain Python.

Rather than require a particular command line launcher that you have to
integrate into, which often makes it difficult to mix local and remote tasks,
pepperssh is only a library.  (However, if you'd like something to do that part
too, have a look at the [runtasks](https://gitlab.com/mkleehammer/runtasks)
project which I also wrote.  I use it as my task runner for Python projects and
now I use pepperssh inside those tasks.)

I know other projects have a lot of great features that pepperssh does not
(yet!), but this tiny library gets the job done in a very maintainable way.  If
you have suggestions, but all means open
an [issue](https://gitlab.com/mkleehammer/pepperssh/issues).


