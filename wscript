#!/usr/bin/env python
# encoding: utf-8

# Import necessary python modules
import os

# Import helper from waf
import Scripting

# Import canonical version from isoquery
from isoquery import __version__

APPNAME = 'isoquery'
VERSION = __version__

top = '.'
out = 'build'

Scripting.excludes.append('.eric4project')
Scripting.excludes.append('.ropeproject')
Scripting.excludes.append('debian')
Scripting.excludes.append('isoquery.e4p')

def set_options(opt):
    # Options for disabling pyc or pyo compilation
    opt.tool_options('python')
    # Support usual directory variables like MANDIR, DATADIR, etc.
    opt.tool_options('gnu_dirs')

def configure(conf):
    # Check that required programs are available
    conf.find_program('msgfmt', var='MSGFMT', mandatory=True)
    conf.check_tool('python')
    conf.check_python_version((2,4))
    conf.check_tool('gnu_dirs')

def build(bld):
    # Compile python files
    obj = bld.new_task_gen('py')
    obj.find_sources_in_dirs('./isoquery')
    obj.install_path = os.path.join('${PYTHONDIR}', 'isoquery')
    # Register installation paths
    bld.install_files('${BINDIR}', [os.path.join('bin', 'isoquery')])
    bld.install_files(os.path.join('${MANDIR}', 'man1'),
                      [os.path.join('man', 'isoquery.1')])
    bld.install_files(os.path.join('${MANDIR}', 'de', 'man1'),
                      [os.path.join('man', 'de', 'isoquery.1')])
    bld.install_files('${DOCDIR}', ['ChangeLog', 'README', 'TODO', 'AUTHORS'])
    # Generate .mo files
    for translation in bld.path.ant_glob(os.path.join('po', '*.po')).split():
        # Get locale from basename of the file, without extension (.po)
        locale = os.path.basename(translation)[:-3]
        # Create a task for each translation file
        mo_file = bld(
            source = translation,
            target = translation.replace('.po', '.mo'),
            rule = bld.env['MSGFMT'] + ' --check --output ${TGT} ${SRC}',
        )
        # The file needs a new name for installation
        bld.install_as(
            os.path.join('${LOCALEDIR}', locale, 'LC_MESSAGES', 'isoquery.mo'),
            mo_file.target
        )
