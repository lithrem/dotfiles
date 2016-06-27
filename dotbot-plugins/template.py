from __future__ import print_function

import os
import subprocess
import sys
import shutil
import fileinput

import dotbot
from dotbot.messenger.color import Color

#TODO:  Overwrite option

class Template(dotbot.Plugin):
    '''
    Substitute values in a file
    '''

    _directive = 'template'

    def can_handle(self, directive):
        return directive == self._directive

    def handle(self, directive, data):
        if directive != self._directive:
            raise ValueError('Template cannot handle directive %s' % directive)
        return self._process_replacements(data)

    def _process_replacements(self, remplacements):
        success = True
        for destination, template in remplacements.items():
            source = os.path.expandvars(template.get('path', False))
            values = os.path.expandvars(template.get('values', False))
            destination = os.path.expandvars(destination)
            force = False
            relative = False
            path = source
            if force:
                success &= self._delete(path, destination, relative, force)
            success &= self._copy(path, destination, relative)
            success &= self._replace(destination, values)
        if success:
            self._log.info('All templates have been set up')
        else:
            self._log.error('Some templates were not successfully set up')
        return success

    def _is_link(self, path):
        '''
        Returns true if the path is a symbolic link.
        '''
        return os.path.islink(os.path.expanduser(path))

    def _exists(self, path):
        '''
        Returns true if the path exists.
        '''
        path = os.path.expanduser(path)
        return os.path.exists(path)

    def _replace(self, path, data):
        path = os.path.expanduser(path)
        f = fileinput.FileInput(path, inplace=True)
        success = True
        for line in f:
            for find, replace in data.items():
                if replace == '__DOTFILES__':
                    replace = self._context.base_directory()
                print(line.replace(find, replace), end='')
        f.close()
        return success

    def _copy(self, source, destination, relative):
        '''
        Copies source to destination.

        Returns true for successfully copied files.
        '''

        success = False
        destination = os.path.expanduser(destination)

        absolute_source = os.path.join(self._context.base_directory(), source)

        if relative:
            source = self._relative_path(absolute_source, destination)
        else:
            source = absolute_source

        if (not self._exists(destination) and self._is_link(destination)):
            self._log.warning('File ls already a link %s' %
                              (destination))

        # we need to use absolute_source below because our cwd is the dotfiles
        # directory, and if source is relative, it will be relative to the
        # destination directory
        elif not self._exists(destination) and self._exists(absolute_source):
            try:
                shutil.copyfile(source, destination)
            except IOError:
                self._log.warning('Copying failed %s -> %s' %
                                  (source, destination))
            else:
                self._log.lowinfo('Creating copy %s -> %s' %
                                  (source, destination))
                success = True
        elif self._exists(destination):
            self._log.warning('%s already exists' % destination)
        # again, we use absolute_source to check for existence
        elif not self._exists(absolute_source):
            self._log.warning('Nonexistent source for %s : %s' %
                              (destination, source))
        else:
            self._log.lowinfo('Link exists %s -> %s' % (destination, source))
            success = True

        return success
