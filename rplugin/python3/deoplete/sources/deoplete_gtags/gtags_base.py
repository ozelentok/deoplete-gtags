import subprocess
import deoplete.util # pylint: disable=locally-disabled, import-error
from deoplete.source.base import Base # pylint: disable=locally-disabled, import-error

class GtagsBase(Base):

    GTAGS_DB_NOT_FOUND_ERROR = 3

    def exec_global(self, search_args, context):
        command = ['global', '--quiet', '--completion'] + search_args
        global_proc = subprocess.Popen(command,
                                       cwd=context['cwd'],
                                       universal_newlines=True,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
        try:
            output, err_output = global_proc.communicate(timeout=15)
        except subprocess.TimeoutExpired:
            global_proc.kill()
            output, err_output = global_proc.communicate()
        global_exitcode = global_proc.returncode

        # Not every project will include a GTAGS file...
        if global_exitcode == self.GTAGS_DB_NOT_FOUND_ERROR:
            return []

        if global_exitcode != 0:
            self.print_global_error(global_exitcode, err_output)
            return []

        return [t for t in output.split('\n') if len(t) > 0]

    def print_global_error(self, global_exitcode, err_output):
        if global_exitcode == 1:
            error_message = '[deoplete-gtags] Error: file does not exists'
        elif global_exitcode == 2:
            error_message = '[deoplete-gtags] Error: invalid arguments\n{}'.format(err_output)
        elif global_exitcode == 3:
            error_message = '[deoplete-gtags] Error: GTAGS not found'
        elif global_exitcode == 126:
            error_message = '[deoplete-gtags] Error: permission denied\n{}'.format(err_output)
        elif global_exitcode == 127:
            error_message = '[deoplete-gtags] Error: \'global\' command not found\n{}'
        else:
            error_message = '[deoplete-gtags] Error: global command failed\n{}'.format(err_output)
        deoplete.util.error(self.vim, error_message)
