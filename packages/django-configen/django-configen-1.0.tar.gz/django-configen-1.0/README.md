# django-configen

A Django app for generating server configuration files, such as for Nginx, 
uWSGI, Gunicorn etc. in a DRY way. 

## Introduction

**The problem:**

Configuration files stay pretty much the same for different projects. You're 
often copying these config files from other projects and then only modifying 
the file paths, domain name and other variables which are unique to this 
project.

This process is error-prone and repetitive. 

**The solution:**

This app solves it by generating config files from templates. So, instead 
of maintaining config files, you maintain their templates. And then use this 
app to render the templates with the project specific variables.

You can copy the original templates to multiple projects and stay assured that 
final generated config files will have appropriate paths and other variables.

## Installation

    pip install django-configen

Add `configen` to `INSTALLED_APPS` list:

```python
INSTALLED_APPS = [
    # ... 
    'configen',
]
```

Add these settings to configure configen:

```python
# where configen will look for config templates
CONFIGEN_TEMPLATES_DIR = os.path.join(BASE_DIR, 'configs/templates')

# where configen will keep the generated files
CONFIGEN_OUTPUT_DIR = os.path.join(BASE_DIR, 'configs/output')

# config context processors
CONFIGEN_CONFIG_PROCESSORS = [
    'configen.config_processors.common',
]
```


`CONFIGEN_CONFIG_PROCESSORS` is a list of config processor functions. They are 
similar to Django's context processors and whatever data they return will be 
made available to the config templates during compiling. 

## Basic usage

The config processor that you just configured above 
(`configen.config_processors.common`), 
makes some common and helpful variables available for you in the config templates.

These variables are:

 + `settings`: current settings file.
 + `project_dir_name`: name of the project directory
 + `virtualenv`: path to current virtualenv.
 + `python_interpreter`: path to current python interpreter

Now you can write templates for your config files using Django's template 
syntax.

For this example, you can create an `nginx.conf` inside `configs/templates/` 
directory and put this code in it:

    server {

        location /media  {
            alias {{ settings.MEDIA_ROOT }};
        }

        location /static {
            alias {{ settings.STATIC_ROOT }};
        } 
    }

Run this command to compile the template:

    python manage.py configen

It will generate the configuration file from the given template and populate 
it with the given variables. The generated file will be inside the 
`configs/output` directory.

## Providing extra context variables

A quick way to provide extra context variables is by using 
`CONFIGEN_DEFAULT_CONTEXT` setting:

```python
CONFIGEN_DEFAULT_CONTEXT = {
    '*': {
        # variables listed here will be available to 
        # all templates
        'project_name': 'example',
    },
    'nginx.conf': {
        # variables listed here will be available only to
        # nginx.conf template
        'domain': 'example.com',
    },
    'uwsgi.ini': {
        # variables listed here will be available only to
        # uwsgi.ini template
        'module': 'myproject.wisgi',
    }
}
```

It should be mentioned that the context returned by `CONFIGEN_DEFAULT_CONTEXT` 
will be overridden by context variables returned by config processors if the 
names collide.

## Writing custom config processor functions

Using `CONFIGEN_DEFAULT_CONTEXT` settings gives you a quick and basic way 
to provide context variables to the templates. However, if you want to do some 
extra calculations before returning the variables, this pattern becomes limiting.

For those cases, configen supports providing context data from functions. 
It works  similar to Django's context processors. However, to avoid name 
confusion, we call them config processors.

This is what a config processor function looks like:

```python
def config_processor(template_name, *args):
    return {'var': 'hello'}
```

The config processor will be passed a `template_name` argument which will let it 
it know the name of the template being compiled. This is useful if you want to 
return different data depending on the template. 

To use your config processor, add this to your settings:

```python
CONFIGEN_CONFIG_PROCESSORS = [
    'configen.config_processors.common',
    'path.to.config_processor',
]
```

The order in which you list the config processors matters. The last config 
processor will override the context variables from the previous processors in 
case there are name collisions.

If you run the `configen` command again, the variables returned by your config 
processor will be available to the config templates.

### Passing arguments to config processors from command line

You can pass extra arguments to your config processors from command line using 
the `--extra` command option:

    python manage.py configen --extra arg1 arg2

These arguments will be available under `args` argument in your config processor.

See documentation for [`--extra`](#--extra) option for more.


## Changing the name of the output file

Configen will save the output files with same name as the input template files. 
This is okay if you have a single project but can become problematic if you 
have multiple projects. 

Suppose, you have two projects and both have a config template called `nginx.conf`. 
The generated config files will also be called `nginx.conf` for both projects. 
Now you can't copy both of these files in Nginx's config directory because of 
the name collision. 

So the general workaround for this problem to rename the files with the project 
name, like `project1_nginx.conf`, `project2_nginx.conf` and this problem is 
solved.

Configen provides two ways to change the name of the output file.

First, the simple way: Using `CONFIGEN_DEFAULT_META` setting:

```python
CONFIGEN_DEFAULT_META = {
    '*': {
        'outfile': 'project1_{template_name}'
    }
}
```

`{template_name}` will be automatically replaced by the name of the template 
including the file extension. 

Just like with `CONFIGEN_DEFAULT_CONTEXT` setting, you can create keys 
with the names of your config templates if you only want to override a particular 
template's output file name.

Another way to provide the meta data to configen is by returning a second dict from your 
config processor like this:

```python
def config_processor(template_name, *args):
    context = {'var': 'hello'}

    meta = {'outfile': 'project1_%s' % template_name}

    return (context, meta)
```

Currently, there's only one option supported for meta data - `outfile`. 


## Settings

### `CONFIGEN_TEMPLATES_DIR`

Path to the directory where configen will look for the config templates.

### `CONFIGEN_OUTPUT_DIR`

Path to the directory where configen will keep the generated config files.

### `CONFIGEN_CONFIG_PROCESSORS`

A list containing Python path to functions which will be called during generation 
of each config template.

Example:

```python
CONFIGEN_CONFIG_PROCESSORS = [
    'configen.config_processors.common',

    'your.custom.processor',
]
```

The `configen.config_processors.common` config processor provided by configen 
makes some commonly used variables available to you in your config templates:

 + `settings`: current settings file.
 + `project_dir_name`: name of the project directory
 + `virtualenv`: path to current virtualenv.
 + `python_interpreter`: path to current python interpreter

You can override these variables from your custom config processors, or leave 
this processor out of the setting if you don't want it. 

### `CONFIGEN_DEFAULT_CONTEXT`

A dictionary containing default context variables for generating config files.

Example:

```python
CONFIGEN_DEFAULT_CONTEXT = {
    '*': {
        # will be passed to all templates 
        'project_name': 'Example',
    },
    'nginx.conf': {
        # will be passed only to nginx.conf template
        'domain': 'example.com',
    },
    'uwsgi.ini': {
        'socket': '/tmp/example.sock',
    },
}
```

### `CONFIGEN_DEFAULT_META`

A dictionary for providing meta configuration information to configen about a 
template.

Currently only option supported is `outfile`. 

Example:

```python
CONFIGEN_DEFAULT_META = {
    '*': {
        # will be used for all templates 
        'outfile': 'myproject_{template_name}',
    },
    'nginx.conf': {
        # will be used only for nginx.conf template
        'outfile': 'myproject_nginx_blah_blah.conf',
    },
}
```

## Command line options

### `template`

Optional. Name of the template to compile. It should be relative to the path 
set in `CONFIGEN_TEMPLATES_DIR` setting. If not provided, all the templates 
present in the directory set by `CONFIGEN_TEMPLATES_DIR` setting are compiled.

Example:

    python manage.py configen nginx.conf


### `--print`

Print the compiled template to stdout. Useful if you want to inspect the output 
without creating/overwriting the output file.

Example:

    python manage.py configen --print


### `--extra`

Extra arguments that you want to pass to your config processor functions.

Example:

    python manage.py configen --extra arg1 arg2


And then access these arguments like this:

```python
def config_processor(template_name, *args):
    print(args)
    # output: ('arg1', 'arg2',)
```

**Important:** Doing `--extra arg1=hello arg2=world` will not work like you 
would expect. `arg1=hello` will be parsed as a whole, instead of argument name 
and value. 

The value your config processor will recieve is this:

```python
def config_processor(template_name, *args):
    print(args)
    # output: ('arg1=hello', 'arg2=world',)
```

Hence, we used the word "arguments" and not "keyword-arguments". You can't pass 
arbitrary named keyword arguments via command line, at least not with `argparse` 
which is used by Django to parse commands.

If you want to be able to receive named keyword arguments, you'll need to parse 
these arguments yourself.


### `--verbosity`

The command will print some debug output while compiling templates. You can turn 
it off like this:

    python manage.py configen --verbosity 0


## License

[BSD-3-Clause](LICENSE.txt)